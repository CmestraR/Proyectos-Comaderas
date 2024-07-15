# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import uuid
from hashlib import md5
from werkzeug import urls

from odoo import api, fields, models, _

from odoo.addons.payment_wompi.const import SUPPORTED_CURRENCIES
_logger = logging.getLogger(__name__)


class PaymentProviderWompi(models.Model):
    _inherit = 'payment.provider'

    @api.model
    def _get_compatible_providers(self, *args, currency_id=None, **kwargs):
        """ Override of payment to unlist PayUmoney providers when the currency is not INR. """
        providers = super()._get_compatible_providers(*args, currency_id=currency_id, **kwargs)

        currency = self.env['res.currency'].browse(currency_id).exists()
        if currency and currency.name not in SUPPORTED_CURRENCIES:
            providers = providers.filtered(lambda p: p.code != 'wompi')

        return providers



    code = fields.Selection(selection_add=[
        ('wompi', 'Wompi Bancolombia')
    ], ondelete={'wompi': 'set default'})
    wompi_prod_merchant_id = fields.Char(string="Wompi public-key(Prod)", required_if_provider='wompi', groups='base.group_user')
    wompi_test_merchant_id = fields.Char(string="Wompi public-key(Test)", required_if_provider='wompi', groups='base.group_user')
    
    def _get_wompi_urls(self, environment):
        """ Wompi URLs"""
        if environment == 'prod':
            return 'https://checkout.wompi.co/p/'
        return 'https://checkout.wompi.co/p/'

    def _wompi_generate_sign(self, inout, values):
        if inout not in ('in', 'out'):
            raise Exception("Type must be 'in' or 'out'")

        if inout == 'in':
            data_string = ('~').join((self.wompi_prod_merchant_id if self.state == 'prod' else self.wompi_test_merchant_id, values['referenceCode'],
                                      str(values['amount']), values['currency']))
        else:
            data_string = ('~').join((self.wompi_prod_merchant_id if self.state == 'prod' else self.wompi_test_merchant_id, values['referenceCode'],
                                      str(values.get('TX_VALUE')), values['currency']))
        return md5(data_string.encode('utf-8')).hexdigest()

    def wompi_form_generate_values(self, values):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        tx = self.env['payment.transaction'].search([('reference', '=', values.get('reference'))])
        currncy= self.env['res.currency'].browse(values.get('currency_id'))
        partner=self.env['res.partner'].browse(values.get('partner_id'))
        phone = ''
        if partner.phone:
            phone = partner.phone
        elif partner.mobile:
            phone = partner.mobile
        # wompi will not allow any payment twise even if payment was failed last time.
        # so, replace reference code if payment is not done or pending.
        if tx.state not in ['done', 'pending']:
            tx.reference = str(uuid.uuid4())
        wompi_values = dict(
            values,
            merchantId=self.wompi_prod_merchant_id if self.state == 'prod' else self.wompi_test_merchant_id,
            description=values.get('reference'),
            referenceCode=tx.reference,
            amount=int(values['amount'] * 100.0),
            tax='0',  # This is the transaction VAT. If VAT zero is sent the system, 19% will be applied automatically. It can contain two decimals. Eg 19000.00. In the where you do not charge VAT, it should should be set as 0.
            taxReturnBase='0',
            currency=currncy.name,
            buyerEmail=partner.email,
            buyerName=partner.name,
            buyerPhone=phone,
            responseUrl=urls.url_join(base_url, '/payment/wompi/response'),

        )
        wompi_values['signature'] = self._wompi_generate_sign("in", wompi_values)
        wompi_values['referenceCode'] = f"{wompi_values['referenceCode']}|{wompi_values['signature']}"
        return wompi_values

    def wompi_get_form_action_url(self):
        self.ensure_one()
        environment = 'prod' if self.state == 'enabled' else 'test'
        return self._get_wompi_urls(environment)


    #def _get_default_payment_method_id(self):
    #    self.ensure_one()
    #    if self.provider != 'wompi':
    #        return super()._get_default_payment_method_id()
    #    return self.env.ref('payment_wompi.payment_method_wompi').id


