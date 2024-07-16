# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import date
import math


class Credit(models.Model):
    _name = 'credit'

    name = fields.Char(
        compute="asign_name",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    
    #Crear botón "Activo"
    active = fields.Boolean(default=True)
     
    res_partner_id = fields.Many2one(
        'res.partner',
        required=True,
        string="Client"
    )
    credit_type_id = fields.Many2one(
        'credit.type',
        index=True,
    )
    modality = fields.Selection(
        [
            ('revolving', 'Revolving'),
            ('amortized', 'Amortized')
        ],
        index=True,
        required=True
    )
    number_credit = fields.Float(
        required=True,
        digits=(17, 0)
    )
    credit_limit = fields.Float(
        string="Base Value of Credit",
        required=True
    )
    available_balance = fields.Float(compute="_compute_available_balance")
    state = fields.Selection(
        [
            ('active', 'Active'),
            ('in_debt', 'In Debt'),
            ('paid_out', 'Paid out')
        ],
        compute="_compute_state",
        index=True,
        default="active"
    )
    sponsoring_entity_id = fields.Many2one(
        'res.bank',
        index=True,
        required=False
    )
    
    quota_month = fields.Float(
        string="Cuota Mensual",
        required=False
    )

    term_months = fields.Integer()
    credit_value_accounted = fields.Float(compute="_compute_available_balance")
    endorsement_commission = fields.Float()
    endorsement_value_plus_vat = fields.Float()
    disbursement_date = fields.Date()
    credit_lines = fields.One2many(
        'credit.line', 'credit_id', string="Credit Lines"
    )
    client_type = fields.Selection(
        [
            ('natural', 'Natural person'),
            ('legal', 'Legal person')
        ],
        default='natural',
        required=True    
    )
    invoice_number = fields.Char(
        string="Invoice Number",
    )

    def _compute_state(self):
        for record in self:
            record.state = 'active'
            if record.available_balance >= record.credit_limit:
                record.state = 'active'


    def _compute_available_balance(self):
        amount_residual = 0
        amount_residual_nc = 0
        amount_capital = 0
        amount_accounted = 0
        for record in self:
            if record.modality == 'amortized':
                for line in record.invoice_ids:
                    if line.state in ['posted']:
                        if line.move_type not in ['out_refund']:
                            amount_residual += line.amount_total_signed
                        else:
                            amount_residual_nc += line.amount_total_signed

                record.available_balance = record.credit_limit - amount_residual - amount_residual_nc
            else:
                for line in record.credit_lines:
                    if line.receipt_id.payment_flow_id:
                        amount_capital += line.capital_subscription
                #record.available_balance = record.credit_limit - amount_capital
                record.available_balance = amount_capital
                if record.available_balance < 0:
                    record.available_balance = 0

                amount_accounted = record.credit_limit

            if record.invoice_ids:
                amount_accounted = sum([x.amount_total_signed for x in record.invoice_ids])

            record.credit_value_accounted = amount_accounted        


    @api.onchange('res_partner_id', 'number_credit')
    def asign_name(self):
        for rc in self:
            if rc.res_partner_id:
                rc.name = (
                    f'{rc.res_partner_id.name} - '
                    f'{int(rc.number_credit)}'
                )

    @api.onchange('credit_type_id')
    def _onchange_credit_type_id(self):
        return {
            'domain': {
                'sponsoring_entity_id': [
                    (
                        'id', 'in', self.mapped(
                            'credit_type_id.supporting_entity_ids.id'
                        )
                    )
                ]
            }
        }

    """@api.onchange('endorsement_commission', 'credit_limit')
    def _calculate_endorsement_value_plus_vat(self):
        self.ensure_one()
        percentage_endorsement_commission = (
            self.credit_limit * (self.endorsement_commission / 100)
        )
        self.endorsement_value_plus_vat = (
            percentage_endorsement_commission
        )"""

    @api.onchange('credit_limit', 'endorsement_value_plus_vat')
    def _calculate_credit_value_accounted(self):
        self.ensure_one()
        self.credit_value_accounted = (
            self.credit_limit + self.endorsement_value_plus_vat
        )

    def verify_fields_for_calculate_payment_schedule(self):
        self.ensure_one()
        if (
            not self.disbursement_date or
            not self.term_months or
            not self.credit_limit
        ):
            raise ValidationError(
                _(
                    "It is necessary to fill in the following fields:"
                    "\n(disbursement_date, term_months, base_value_credit"
                )
            )
    @api.onchange('credit_limit', 'endorsement_commission', 'term_months')
    def _calculate_quota_month(self):
        self.ensure_one()
        if self.term_months == 0 or self.endorsement_commission == 0:
            self.quota_month = 0
        else:
            self.quota_month = (
                (self.endorsement_commission / 100) * self.credit_limit /
                (1 - (1 + (self.endorsement_commission / 100)) ** -self.term_months)
            )
        
    @api.onchange('quota_month', 'credit_limit','term_months')
    def _calculate_endorsement_value_plus_vat(self):
        self.ensure_one()
        self.endorsement_value_plus_vat = (
            (self.quota_month*self.term_months)-self.credit_limit
        )    

    def calculate_payment_schedule(self):
        self.ensure_one()
        self._context.get('force_delete')
        old_credit_lines = self.env['credit.line'].search(
            [('credit_id', '=', self.id)]
        )
        old_credit_lines.with_context(force_delete=True).unlink()
        self.verify_fields_for_calculate_payment_schedule()
        payment_date = self.disbursement_date
        balance = self.credit_limit
        quota = self.quota_month
        total_paid_capital = 0
        for i in range(1, self.term_months + 1):
            payment_date += relativedelta(months=1)
            if i==1:
                interest = max(0, (self.endorsement_commission / 100) * self.credit_limit)
                payment_capital = max(0, quota - interest)
            else:
                interest = max(0, (self.endorsement_commission / 100) * balance)
                payment_capital = max(0, quota - interest)
                
            total_paid_capital += payment_capital
            balance = max(0, self.credit_limit - total_paid_capital)
            if i == self.term_months:
                balance = 0    
            self.env['credit.line'].create(
                {
                    'credit_id': self.id,
                    'payment_date': payment_date,
                    'installment_number': i,
                    'capital_subscription': payment_capital,
                    'bank_interest': interest,
                    'amount_to_be_paid': interest + payment_capital,
                    'capital_balance': balance,
                }
            )
        # Create receipts for each credit line
        self.create_lines_receipts()

    # Create receipts for each credit line
    def create_lines_receipts(self):
        self.ensure_one()
        for line in self.credit_lines:
            line.create_receipt()

    # Update notes in each line's receipt
    @api.onchange('credit_type_id', 'number_credit', 'invoice_number')
    def _update_receipts_notes(self):
        self.ensure_one()
        for line in self.credit_lines:
            if line.receipt_id:
                if self.invoice_number:
                    receipt_notes = _("""Credit Data:
                        Invoice Number: %s
                        Credit type: %s
                        Credit Number: %s\n""") % (
                            self.invoice_number,
                            self.credit_type_id.name,
                            self.number_credit,
                        )
                else:
                    receipt_notes = _("""Credit Data:
                        Credit type: %s
                        Credit Number: %s\n""") % (
                            self.credit_type_id.name,
                            self.number_credit,
                        )
                line.receipt_id.write({
                    'narration': receipt_notes,
                    'ref': self.invoice_number or '',
                })

    # Publish receipts related with the credit
    def publish_receipts(self):
        self.ensure_one()
        for line in self.credit_lines:
            if line.receipt_id:
                line.receipt_id.action_post()
    
    def check_credit_line_status(self):
        credit_ids = self.env['credit'].search([
            ('state', 'in', ['active', 'in_debt'])
        ])
        for credit in credit_ids:
            credit_paid = True
            credit_in_debt = False
            for line in credit.credit_lines:
                if line.receipt_id:
                    if line.receipt_id.amount_residual:
                        credit_paid = False
                        if line.receipt_id.invoice_date_due < date.today():
                            credit_in_debt = True
                else:
                    credit_paid = False

            if credit_paid:
                credit.state = 'paid_out'
            elif credit_in_debt:
                credit.state = 'in_debt'
            else:
                credit.state = 'active'

    def unlink(self):
        for record in self:
            lines = record.credit_lines
            published_receipts = [
                x.receipt_id for x in lines if x.receipt_id.state == 'posted'
            ]
            if published_receipts:
                raise ValidationError(
                    _("You can't delete credits with receipts published.")
                )
            for line in lines:
                models.Model.unlink(line)
        return models.Model.unlink(self)


class CreditLine(models.Model):
    _name = 'credit.line'

    name = fields.Char(
        compute="_asign_name",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )

    credit_id = fields.Many2one(
        'credit',
        readonly=True
    )
    company_currency_id = fields.Many2one(
        'res.currency',
        string='Company Currency',
        readonly=True,
        default=lambda self: self.env.company.currency_id
    )
    payment_date = fields.Date()
    installment_number = fields.Integer()
    capital_subscription = fields.Monetary(
        currency_field='company_currency_id'
    )
    bank_interest = fields.Monetary(currency_field='company_currency_id')
    amount_to_be_paid = fields.Monetary(currency_field='company_currency_id')
    capital_balance = fields.Monetary(currency_field='company_currency_id')
    receipt_id = fields.Many2one(
        comodel_name='account.move',
        string="Receipt",
    )

    # Unlink receipt related
    def unlink(self):
        if self.receipt_id:
            self.receipt_id.unlink()
        return super(CreditLine, self).unlink()

    @api.onchange('credit_id', 'installment_number')
    def _asign_name(self):
        for record in self:
            if record.credit_id and record.installment_number:
                record.name = (
                    f'{record.installment_number} - '
                    f'{record.credit_id.name}'
                )

    # Create receipts to record pays
    def create_receipt(self):
        self.ensure_one()
        if self.credit_id.invoice_number:
            receipt_notes = _(
                """Credit Data:
                Invoice Number: %s
                Credit type: %s
                Credit Number: %s\n""") % (
                    self.credit_id.invoice_number,
                    self.credit_id.credit_type_id.name,
                    self.credit_id.number_credit,
                )
        else:
            receipt_notes = _("""Credit Data:
                Credit type: %s
                Credit Number: %s\n""") % (
                    self.credit_id.credit_type_id.name,
                    self.credit_id.number_credit,
                )

        product = self.env.ref(
            'allocation_of_credit_amount.payment_of_credits_product'
        )
        interest = self.env.ref(
            'allocation_of_credit_amount.interest_of_credit_product'
        )
        """life_insurance = self.env.ref(
            'allocation_of_credit_amount.life_insurance_product'
        ) """
        dairy_ref = self.env.ref(
            'allocation_of_credit_amount.payment_of_credits_dairy'
        )

        # Customer assignment
        if self.credit_id.credit_type_id.receivable != 'bank':
            assigned_partner = self.credit_id.res_partner_id.id
        else:
            assigned_partner = self.credit_id.sponsoring_entity_id.partner_id.id

        receipt_vals = {
            'invoice_date': self.payment_date, #date.today(),
            'invoice_date_due': self.payment_date,
            'partner_id': assigned_partner,
            'move_type': 'out_receipt',
            'ref': self.credit_id.invoice_number,
            'journal_id': dairy_ref.id,
            'narration': receipt_notes,
            'company_id': self.env.company.id,
            'credit_payment': True,
            'credit': self.credit_id.id
        }
        
        receipt = self.env['account.move'].create(receipt_vals)

        receipt_lines_vals = {
            'product_id': product.id,
            'price_unit': self.capital_subscription,
            #'account_id': dairy_ref.default_account_id.id,
            'quantity': 1,
            'price_subtotal': self.capital_subscription,
            #'exclude_from_invoice_tab': False,
            'date_maturity': self.payment_date,
        }
        receipt_lines_vals_2 = {
            'product_id': interest.id,
            'price_unit': self.bank_interest,
            #'account_id': dairy_ref.default_account_id.id,
            'quantity': 1,
            'price_subtotal': self.bank_interest,
            #'exclude_from_invoice_tab': False,
            'date_maturity': self.payment_date,
        }
        """receipt_lines_vals_3 = {
            'product_id': life_insurance.id,
            'price_unit': self.capital_subscription * 0.03,
            'account_id': dairy_ref.default_account_id.id,
            'quantity': 1,
            'price_subtotal': self.capital_subscription * 0.03,
            #'exclude_from_invoice_tab': False,
            'date_maturity': self.payment_date,
        }"""
        receipt.write({
            'invoice_line_ids': [(0, 0, receipt_lines_vals),(0, 0, receipt_lines_vals_2),"""(0, 0, receipt_lines_vals_3)"""],
            'credit_line_id': self.id,
        })

        receipt_line = receipt.invoice_line_ids[0]
        receipt._recompute_invoice_date_due_receipt(self)
        for line in receipt.line_ids:
            line.write({
                'date_maturity': self.payment_date,
            })
        self.receipt_id = receipt.id
          
#---Create receipt for disbursement --------------------------------------------------20231022
    def create_receipts_disbursement(self):
        partner = self.res_partner_id
        if not partner:
            raise UserError(_("No se ha especificado un cliente para este crédito."))

        disbursement_product = self.env.ref(
            'allocation_of_credit_amount.disbursement_product'
        )
        dairy_disbursement_ref = self.env.ref(
            'allocation_of_credit_amount.disbursement_of_credits_dairy'
        )
         
        # Crear un recibo de tipo 'in_receipt' asociado al cliente
        d_receipt_vals = {
            'invoice_date': fields.Date.today(),
            'partner_id': partner.id,
            'move_type': 'in_receipt',
            'journal_id': dairy_disbursement_ref.id,
        }
        
        d_receipt = self.env['account.move'].create(d_receipt_vals)

        # Crear una línea en el recibo con el valor del 'credit_limit'
        d_receipt_line_vals = {
            'product_id': disbursement_product.id,  # Reemplaza 'your_product_id' por el ID del producto deseado
            'price_unit': self.credit_limit,
            'quantity': 1,
            'price_subtotal':self.credit_limit            
        }
        d_receipt.write({
            'invoice_line_ids': [(0, 0, d_receipt_line_vals)],
        })

        # Publicar el recibo
        d_receipt.action_post()
        
        return d_receipt