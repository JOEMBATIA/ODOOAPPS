from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_description = fields.Text(string='Product Description')