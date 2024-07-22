from odoo import models, fields, api


class Inventory(models.Model):
    _name = "syscraft.inventory.tbl"
    _description = "Inventory"
    _inherit = "mail.thread"
    _rec_name = "product_id"

    product_id = fields.Many2one('syscraft.product.tbl', string="Product Name ")
    taxes = fields.Selection([('16% VAT', '16% VAT'), ('TAX EXEMPT', 'TAX EXEMPT')], string="Tax ")
    ref_no = fields.Char(string="Reference No.")
    pricce = fields.Float(string="Price", compute='fill_price_field', store=True)
    status = fields.Selection([('in-stock', 'In Stock'), ('outof-stock', 'Out of Stock')])
    Manufacturer_id = fields.Many2one('syscraft.clinic.manufactures.tbl', string="Manufacturer")
    SKU = fields.Selection([('card', 'CARD'), ('box', 'BOX')], string="SKU ")
    quantity = fields.Integer(string="Available Quantity ")
    total_price = fields.Integer(string="Price(incl tax)", compute='compute_total_price', store=True)
    category = fields.Selection([('medicine', 'Medicine'), ('internal', 'Internal'), ('external', 'External'),
                                 ('external|korea', 'External|Korea'), ('germany', 'Germany'), ('India', 'India'), ('pharmacy', 'Pharmacy')
                                 , ('spain', 'Spain')], string="Category ")

    order_number_date = fields.Date(string="Order No. Date")
    order_status = fields.Selection([('open order', 'open order'), ('closed order', 'closed order')], string="Order status ")
    order_ref_no = fields.Text(string="Order Ref No. ")
    order_supplied_by = fields.Many2one('syscraft.clinic.records.tbl', string="Order supplied by ")
    order_ordered_by = fields.Text(string="Order ordered by ")

    @api.depends('product_id.price', 'pricce', 'taxes')
    def compute_total_price(self):
        for rec in self:
            if rec.product_id.price:
                price = rec.pricce

                if rec.taxes == '16% VAT':
                    total_price = price + (price * 16 / 100)
                else:
                    total_price = price

                rec.total_price = total_price

    @api.depends('product_id.price')
    def fill_price_field(self):
        for rec in self:
            if rec.product_id.price:
                rec.pricce = rec.product_id.price

    class Product(models.Model):
        _name = "syscraft.product.tbl"
        _description = "Product"
        _rec_name = "product"

        product = fields.Char()
        price = fields.Float()

    class Manufacturer(models.Model):
        _name = "syscraft.clinic.manufactures.tbl"
        _description = "Manufacturer Records"

        manufacturer = fields.Char(strng="Manufacturer ")
