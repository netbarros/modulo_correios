{
    'name': 'modulo_correios',
    'version': '1.0',
    'category': 'Delivery',
    'summary': 'Integração completa com os Correios: cálculo de frete, pré-postagem e rastreamento',
    'description': """
### Funcionalidades:
- Cálculo de frete em tempo real.
- Geração de etiquetas de pré-postagem.
- Rastreamento automatizado e manual.
- Validação obrigatória da API antes de ativar o módulo.
- Total compatibilidade com multiempresa e loja virtual.
    """,
    'author': 'Software Lotus by Odoo',
    'website': 'https://www.softwarelotus.com.br',
    'license': 'OPL-1',
    'support': 'https://www.softwarelotus.com.br',
    'price': 199.00,
    'currency': 'EUR',
    'depends': [
        'delivery',
        'sale_management',
        'stock',
        'base_setup',
        'website_sale_delivery'
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/delivery_correios_views.xml',
        'views/correios_service_views.xml',
        'views/correios_config_views.xml',
        'views/dashboard_views.xml',
        'data/delivery_correios_data.xml',
        'data/ir_cron_data.xml',
    ],
    'images': [
        'static/description/icon.png',
        'static/description/screenshot.png'
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'maintainers': ['netbarros'],
    'cloc_exclude': ['tests/'],
}
