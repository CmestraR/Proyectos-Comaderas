# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Copyright (C) David Arnold (XOE Solutions).

# Author        Jose Moreno, yosefeliyahu@gmail.com
# Co-Authors    Firefly-e, info@firefly-e.com

{
    'name': 'Wompi Payment Provider',
    'category': 'Accounting/Payment Providers',
    'sequence': 380,
    'author': "Firefly-e",
    'summary': 'Payment Provider: Wompi Bancolombia Implementation',
    'description': """Wompi payment Provider""",
    'version': '16.0.0.1.1',
    'category': 'Invoicing',
    'license': 'AGPL-3',
    'depends': ['payment'],
    'data': [
        'views/payment_provider_views.xml',
        'views/payment_wompi_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'images': ['static/description/icon.png'],
    'application': True,
    'installable': True,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'assets': {
        'web.assets_frontend': [
            'payment_wompi/static/src/js/payment_form.js',
        ],
    },
    'currency': 'USD',
    'price': 50.00,
}
