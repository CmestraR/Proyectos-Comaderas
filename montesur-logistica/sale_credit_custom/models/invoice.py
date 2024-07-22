# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Invoice(models.Model):
    _inherit = 'account.move'

    credit_payment = fields.Boolean(default=False)
    credit = fields.Many2one(
        'credit',
        string="Credit to use"
    )
    credit_invoice_ids = fields.Many2many(
        'account.move',
        string="Facturas relacionadas",
        compute="_domain_credit_invoice_ids"
    )

    def _domain_credit_invoice_ids(self):
        for record in self:
            if record.credit:
                credit = self.env['credit'].search(
                                            [('id','=',self.credit.id)]
                                            )
                ids_invoice = credit.invoice_ids.ids
                record.credit_invoice_ids = ids_invoice
            else:
                record.credit_invoice_ids = False

    def action_post(self):
        if self.credit_payment and self.credit and self.move_type not in ['out_receipt','out_refund']:
            if (
                self.credit.available_balance < self.amount_total
                or self.credit.state == 'in_debt'
            ):
                raise ValidationError(
                    _(
                        'The invoice cannot be confirmed. '
                        'Possible reasons are as follows:\n'
                        '- The invoice has a value greater than '
                        'the available credit value.\n'
                        '- The client is behind with the credit payments.\n'
                    )
                )
            self.credit.sudo().calculate_expenses_acum()
            self._generate_accounting_notes_type_credit()
        res = super(Invoice, self).action_post()
        return res

    def _generate_accounting_notes_type_credit(self):
        credit_type = self.credit.credit_type_id
        receivable_type = self.env.ref(
            #"account.data_account_type_receivable"
            "account.selection__account_account__account_type__asset_receivable"
        )
        if credit_type.invoicing == 'bank':
            for line in self.line_ids:
                if (
                    line.account_id.user_type_id.id == receivable_type.id
                ):
                    line.update({
                        'partner_id':
                        self.credit.sponsoring_entity_id.partner_id.id
                    })

    def button_draft(self):
        res = super(Invoice, self).button_draft()
        if self.credit_payment and self.credit:
            self.credit.calculate_expenses_acum()
        return res
