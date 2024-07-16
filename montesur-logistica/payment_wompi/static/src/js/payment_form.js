/* global Wompi */
odoo.define('payment_wompi.payment_form_mixin', require => {
    'use strict';

    const checkoutForm = require('payment.checkout_form');
    const manageForm = require('payment.manage_form');

    const wompiMixin = {
        /**
         * Redirect the customer by submitting the redirect form included in the processing values.
         *
         * For a provider to redefine the processing of the payment with redirection flow, it must
         * override this method.
         *
         * @private
         * @param {string} code - The code of the provider
         * @param {number} providerId - The id of the provider handling the transaction
         * @param {object} processingValues - The processing values of the transaction
         * @return {undefined}
         */
        _processRedirectPayment: function (code, providerId, processingValues) {
            if (code !== 'wompi') {
                return this._super(...arguments);
            }
            // Append the redirect form to the body
            const $redirectForm = $(processingValues.redirect_form_html).attr(
                'id', 'o_payment_redirect_form'
            );
            // Ensures external redirections when in an iframe.
            $redirectForm[0].setAttribute('target', '_top');
            $(document.getElementsByTagName('body')[0]).append($redirectForm);
            $redirectForm[0].setAttribute("action", $redirectForm.find('input[name="data_set"]').val());
            // Submit the form
            $redirectForm.submit();
        },
    };

    checkoutForm.include(wompiMixin);
    manageForm.include(wompiMixin);

});
