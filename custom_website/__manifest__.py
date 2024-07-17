{
    'name': "Personalización del Sitio Web",
    'version': "1.0",
    'description': 'Modulo personalizado para agregar funcionalidades y estilos al sitio web',
    'author': 'Negocios e Inversiones Montesur',
    'depends': ['website'],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'custom_website/static/src/js/custom_script.js',
            'custom_website/static/src/css/custom_style.css',
        ],
    },
}
