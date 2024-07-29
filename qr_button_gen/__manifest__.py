{
    'name': "QR Code Generator",
    'version': "1.0.1",
    'depends': ['base', 'sale'],
    'author': "Cristian D. Mestra",
    'category': "Sales",
    'description': """
        Este modulo nos ayuda a crear codigos QR para nuestros enlaces de pago
    """,
    'data': [
        'views/sale_qr_code_view.xml',
    ],
    'installable': True,
    'auto_install': False,


}
