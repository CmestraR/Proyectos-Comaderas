{
    'name': 'WhatsApp Sale Integration',
    'version': '16.0.1.0.0',
    'category': 'Sales',
    'summery': 'Send whatsApp message to the customer with the sale order details.',
    'author': 'INKERP',
    'website': "https://www.INKERP.com",
    'depends': ['sale'],
    'data': [
        'views/sale_order_view.xml',
    ],

    'images': ['static/description/banner.png'],
    'application': True,
    'autoinstall': False,
    'installable': True,
    'license': "OPL-1",
    'price': '14.99',
    'currency': 'USD',
}
