{
    'name': 'Custom Inventory Management',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Custom delivery notes, quality control, POS modifications and stock alerts',
    'description': """
        Custom Inventory Management Module
        ==================================

        Features:
        - Modified delivery note views and fields
        - Enhanced quality control functionality
        - Custom POS view modifications
        - Automated email notifications for minimum stock levels
        - Custom fields and workflows
    """,
    'author': 'Joe Mbatia',
    'website': 'https://joembatiaportfolio.netlify.app',
    'depends': ['stock', 'base', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/email_templates.xml',
        'views/stock_picking_views.xml',
        # 'views/quality_check_views.xml',
        #'views/product_template_views.xml',
        # 'views/pos_config_views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'custom_inventory_management/static/src/js/pos_custom_fields.js',
            'custom_inventory_management/static/src/xml/pos_custom_templates.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}