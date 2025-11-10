from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    custom_description = fields.Text(string='Description')