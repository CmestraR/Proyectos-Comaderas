# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import date
# import numpy_financial as npf


class AccountMove(models.Model):
    _inherit = "account.move"
    
    credit = fields.Many2one('credit', string='Credit')
    
    credit_line_id = fields.Many2one(
        comodel_name='credit.line',
        string='Credit Line'
    )

    def _recompute_invoice_date_due_receipt(self, credit_line):
        if not credit_line.payment_date:
            return
        if self.invoice_date_due != credit_line.payment_date:
            self.invoice_date_due = credit_line.payment_date
            self.invoice_payment_term_id = False
