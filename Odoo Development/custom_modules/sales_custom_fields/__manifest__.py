{
    'name': 'Custom Sales Documents Description',
    'version': '16.0.1.0.0',
    'category': 'Sales',
    'summary': 'Add description field to sales documents',
    'author': 'Joe Mbatia',
    'website': 'https://joembatiaportfolio.netlify.app',
    'depends': ['sale', 'account', 'stock'],
    'data': [
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
}