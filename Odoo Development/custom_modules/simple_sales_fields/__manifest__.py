{
    'name': 'Sales Order Line Description',
    'version': '19.0',
    'category': 'Sales',
    'summary': 'Add description column to sales order lines',
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
        # 'views/account_move_views.xml',
        # 'views/stock_picking_views.xml',
    ],
    'author' : 'Joe Mbatia',
    'installable': True,
    'application': False,
    'auto_install': False,
}