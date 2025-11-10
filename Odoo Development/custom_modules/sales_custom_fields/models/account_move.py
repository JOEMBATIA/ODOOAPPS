from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    custom_description = fields.Text(string='Description')