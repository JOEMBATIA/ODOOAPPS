from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_description = fields.Text(string='Product Description')