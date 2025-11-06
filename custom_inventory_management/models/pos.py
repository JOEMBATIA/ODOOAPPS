from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    custom_receipt_note = fields.Text(string='Receipt Note')
    delivery_preference = fields.Selection([
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery')
    ], string='Delivery Preference', default='pickup')


class PosConfig(models.Model):
    _inherit = 'pos.config'

    # Add any POS configuration fields if needed
    iface_custom_receipt = fields.Boolean(string='Custom Receipt', default=True)