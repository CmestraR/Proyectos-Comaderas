# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import uuid
import requests
from hashlib import md5
from werkzeug import urls

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


_logger = logging.getLogger(__name__)


class PaymentTransactionWompi(models.Model):

    _inherit = 'payment.transaction'
 

    def _get_specific_processing_values(self, processing_values):
        """ Override of payment to return an access token as acquirer-specific processing values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic processing values of the transaction
        :return: The dict of acquirer-specific processing values
        :rtype: dict
        """
        if processing_values.get('provider_code') != 'wompi':
            return super()._get_specific_processing_values(processing_values)

        paymentAcq = self.env['payment.provider'].browse(processing_values.get('provider_id'))
        data_wompi = paymentAcq.wompi_form_generate_values(processing_values)
        return data_wompi

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return Mollie-specific rendering values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic and specific processing values of the transaction
        :return: The dict of acquirer-specific rendering values
        :rtype: dict
        """
        res = super()._get_specific_rendering_values(processing_values)
        if processing_values.get('provider_code') != 'wompi':
            return res

        paymentAcq = self.env['payment.provider'].browse(processing_values.get('provider_id'))
        processing_values.update({"tx_url": paymentAcq.wompi_get_form_action_url()})
        #processing_values['referenceCode'] = processing_values['referenceCode'].split("|")[0].strip()

        return processing_values


    @api.model
    def form_feedback(self, data, acquirer_name):

        if acquirer_name != 'wompi':
            return super(PaymentTransactionWompi, self).form_feedback(data, acquirer_name)

        if data.get('env') == 'test':
            url = f'https://sandbox.wompi.co/v1/transactions/{data.get("id")}'
        else:
            url = f'https://production.wompi.co/v1/transactions/{data.get("id")}'

        resp = requests.get(url)
        if resp.status_code != 200:
            raise ValidationError(_("Wompi service unavailable"))
        else:
            data.update(resp.json())

        invalid_parameters, tx = None, None
        tx_find_method_name = '_%s_form_get_tx_from_data' % acquirer_name
        if hasattr(self, tx_find_method_name):
            tx = getattr(self, tx_find_method_name)(data)

        # TDE TODO: form_get_invalid_parameters from model to multi
        invalid_param_method_name = '_%s_form_get_invalid_parameters' % acquirer_name
        if hasattr(self, invalid_param_method_name):
            invalid_parameters = getattr(tx, invalid_param_method_name)(data)

        if invalid_parameters:
            _error_message = '%s: incorrect tx data:\n' % (acquirer_name)
            for item in invalid_parameters:
                _error_message += '\t%s: received %s instead of %s\n' % (item[0], item[1], item[2])
            return False

        # TDE TODO: form_validate from model to multi
        feedback_method_name = '_%s_form_validate' % acquirer_name
        if hasattr(self, feedback_method_name):
            return getattr(tx, feedback_method_name)(data)
        return True

    @api.model
    def _wompi_form_get_tx_from_data(self, data):
        """ Given a data dict coming from wompi, verify it and find the related
        transaction record. """

        reference, txnid, sign = data["data"].get('reference').split("|")[0].strip(), data.get('id'), data["data"].get('reference').split("|")[1].strip()
        if not reference or not txnid or not sign:
            raise ValidationError(_('Wompi: received data with missing reference (%s) or transaction id (%s) or sign (%s)') % (reference, txnid, sign))

        transaction = self.search([('reference', '=', reference)])

        if not transaction:
            error_msg = (_('Wompi: received data for reference %s; no order found') % (reference))
            raise ValidationError(error_msg)
        elif len(transaction) > 1:
            error_msg = (_('Wompi: received data for reference %s; multiple orders found') % (reference))
            raise ValidationError(error_msg)

        # verify shasign
        data_wompi = {
            "referenceCode": reference,
            "amount": data["data"].get("amount_in_cents"),
            "currency": data["data"].get("currency"),
            "transactionState": data["data"].get("status"),
            "TX_VALUE": data["data"].get("amount_in_cents"),
        }

        sign_check = transaction.provider_id._wompi_generate_sign('out', data_wompi)
        if sign_check.upper() != sign.upper():
            raise ValidationError(('Wompi: invalid sign, received %s, computed %s, for data %s') % (sign, sign_check, data))
        return transaction

    def _wompi_form_get_invalid_parameters(self, data):
        invalid_parameters = []

        if self.provider_reference and data["data"].get('id') != self.provider_reference:
            invalid_parameters.append(('Reference code', data["data"].get('id'), self.provider_reference))
        if float_compare(float(data["data"].get('amount_in_cents', '0.0') / 100) , self.amount, 2) != 0:
            invalid_parameters.append(('Amount', data["data"].get('amount_in_cents') / 100, '%.2f' % self.amount))

        return invalid_parameters

    def _wompi_form_validate(self, data):
        self.ensure_one()

        status = data["data"].get('status')
        res = {
            'provider_reference': data["data"].get('id'),
            'state_message': data["data"].get('status') or ""
        }

        if status == 'APPROVED':
            _logger.info('Validated Wompi payment for tx %s: set as done' % (self.reference))
            res.update(state='done', last_state_change=fields.Datetime.now())
            self._set_done()
            self.write(res)
            self._execute_callback()
            return True
        elif status == 'PENDING':
            _logger.info('Received notification for Wompi payment %s: set as pending' % (self.reference))
            res.update(state='pending')
            self._set_pending()
            return self.write(res)
        elif status in ['VOIDED', 'DECLINED']:
            _logger.info('Received notification for Wompi payment %s: set as Cancel' % (self.reference))
            res.update(state='cancel')
            self._set_canceled()
            return self.write(res)
        else:
            error = 'Received unrecognized status for Wompi payment %s: %s, set as error' % (self.reference, status)
            _logger.info(error)
            res.update(state='cancel', state_message=error)
            self._set_canceled()
            return self.write(res)
