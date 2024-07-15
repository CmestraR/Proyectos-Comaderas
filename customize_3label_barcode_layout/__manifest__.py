{
    'name': 'Customize 3 label printing layout to PDF',
    'version': '16.0.0.0.2',
    'author': 'Ganemo',
    'category': 'Warehouse',
    'website': 'https://www.ganemo.co/demo',
    'summary': 'Configure the three-column label print layout, which can be created in PDF and sent to a ticket printer.',
    'description': '''
    Configure the label printing layout by modifying the height, width, font size and other variables, 
    which will be used to create three-column labels in a PDF file, 
    from which they can be sent to a self-adhesive label printer.
    ''',
    'depends': [
        'product',
        'purchase',
        'stock',
    ],
    'data': [
        'security/barcode_label_security.xml',
        'security/ir.model.access.csv',
        'data/barcode_config.xml',
        'wizard/barcode_labels.xml',
        'views/report_paperformat.xml',
        'views/barcode_config_view.xml',
        'views/report_product_barcode.xml',
        'views/menu_view.xml'
    ],
    'images': ['images/label.jpg'],
    'auto_install': False,
    'installable': True,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 59.00,
}
