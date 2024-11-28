{
    'name': 'Integração Completa com os Correios',
    'version': '1.0',
    'category': 'Logistics/Delivery',
    'summary': 'Cálculo de frete, pré-postagem e rastreamento integrado com os Correios',
    'description': """
### Funcionalidades:
- **Cálculo de Frete:** Obtenha tarifas em tempo real diretamente dos Correios.
- **Pré-postagem:** Geração de etiquetas prontas para envio.
- **Rastreamento Automatizado:** Atualizações periódicas sobre o status das entregas.
- **Compatibilidade Total:** Multiempresa, loja virtual e integração completa com o Odoo 18.
- **Validação de API:** Ativação dependente da validação dos dados do contrato com os Correios.
    """,
    'author': 'Software Lotus by Odoo',
    'website': 'https://www.softwarelotus.com.br',
    'license': 'LGPL-3',
    'support': 'https://www.softwarelotus.com.br/contact',
    'price': 199.00,
    'currency': 'USD',
    'depends': [
        'base',
        'delivery',
        'mail',
        'sale_management',
        'stock',
        'base_setup',
        'website_sale_delivery',
    ],
    'data': [
        # Arquivos de segurança
        'security/security.xml',
        'security/ir.model.access.csv',
        
        # Arquivos de visualização
        'views/menus.xml',
        'views/delivery_correios_views.xml',
        'views/correios_service_views.xml',
        'views/correios_config_views.xml',
        'views/dashboard_views.xml',
        
        # Dados iniciais
        'data/delivery_correios_data.xml',
        'data/ir_cron_data.xml',
    ],
    'images': [
        'static/description/icon.png',
        'static/description/screenshot.png',
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'maintainers': ['netbarros'],
    'cloc_exclude': ['tests/'],
}
