from odoo import models, fields, api
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    custom_delivery_note = fields.Text(string='Delivery Note')
    quality_check_required = fields.Boolean(string='Quality Check Required', default=False)

    def action_confirm(self):
        res = super(StockPicking, self).action_confirm()
        # Check if minimum stock level is reached
        self.check_minimum_stock_level()
        return res

    def check_minimum_stock_level(self):
        product_model = self.env['product.product']
        for move in self.move_ids_without_package:
            product = move.product_id
            if product.qty_available <= product.min_stock_level:
                self.send_stock_alert_email(product)

    def send_stock_alert_email(self, product):
        template = self.env.ref('custom_inventory_management.email_template_min_stock')
        if template:
            template.with_context({
                'product_name': product.name,
                'current_stock': product.qty_available,
                'min_stock_level': product.min_stock_level
            }).send_mail(self.id, force_send=True)