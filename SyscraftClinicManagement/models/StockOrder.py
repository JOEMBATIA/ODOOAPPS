from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class StockOrder(models.Model):
    _name = "syscraft.inventory.stock.order.tbl"
    _description = "Stock Order Records"
    _inherit = "mail.thread"
    _rec_name = "product_id"

    product_id = fields.Many2one('syscraft.product.tbl', string="Product Name ")
    TYPE_id = fields.Many2one('syscraft.clinic.financials.expense.tbl')
    ref_no = fields.Char(string="Reference No.")
    category = fields.Selection([('medicine', 'Medicine'), ('internal', 'Internal'), ('external', 'External'),
                                 ('external|korea', 'External|Korea'), ('germany', 'Germany'), ('India', 'India'), ('pharmacy', 'Pharmacy')
                                 , ('spain', 'Spain')], string="Category ")

    transaction_date = fields.Date(string="Transaction Date ")
    transaction_due_date = fields.Date(string="Transaction Due Date ")
    order_number_date = fields.Date(string="Order No. Date")
    order_status = fields.Selection([('open order', 'open order'), ('closed order', 'closed order')], string="Order status ")
    order_ref_no = fields.Text(string="Order Ref No. ")
    order_supplied_by = fields.Many2one('syscraft.clinic.records.tbl', string="Order supplied by ")
    order_ordered_by = fields.Char()
    comments = fields.Text(string="Internal Comments ")
    voucher_line_ids = fields.One2many('syscraft.stock.order.tbl', 'stock_order_id')

    def action_open_expense_voucher(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'syscraft.clinic.financials.expense.tbl',  # Replace with your actual patient model
            'view_mode': 'form',
            'view_id': self.env.ref('SyscraftClinicManagement.view_expense_form').id,
            # Replace with your actual view ID
            'target': 'current',
            'res_id': self.TYPE_id.id,  # Replace with the field containing patient ID
        }

    def action_open_stock_order(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'syscraft.inventory.stock.order.tbl',  # Replace with your actual patient model
            'view_mode': 'form',
            'view_id': self.env.ref('SyscraftClinicManagement.view_stock_order_form').id,
            # Replace with your actual view ID
            'target': 'current',
            'res_id': self.product_id.id,  # Replace with the field containing patient ID
        }


class StockOrderVoucherItems(models.Model):
    _name = 'syscraft.stock.order.tbl'
    _description = 'Stock Order Voucher Items'

    item_id = fields.Many2one('syscraft.stock.order.items.tbl')
    pk = fields.Char()
    free_pk = fields.Char()
    pk_buying_price = fields.Float()
    discount = fields.Float()
    pk_selling_price = fields.Float()
    total_price = fields.Float()
    quantity = fields.Integer()
    taxes = fields.Selection([('16% VAT', '16% VAT'), ('TAX EXEMPT', 'TAX EXEMPT')], string="Tax ")
    stock_order_id = fields.Many2one('syscraft.inventory.stock.order.tbl')

    @api.depends('quantity', 'item_id.price', 'discount')
    def compute_total(self):
        for rec in self:
            try:
                if rec.item_id.price:
                    discounted_price = (rec.discount / 100) * rec.item_id.price
                    price = rec.item_id.price - discounted_price
                    total_price = rec.quantity * price
                    rec.total = total_price
                else:
                    rec.total = 0.0  # Set a default value if needed
            except Exception as e:
                rec.total = 0.0  # Handle any exceptions and set a default value
                _logger.error(f"Error in compute_total: {e}")

    # @api.onchange('item_id')
    # def fill_price_field(self):
    #     if self.item_id:
    #         self.price = self.item_id.price


class VoucherItens(models.Model):
    _name = 'syscraft.stock.order.items.tbl'
    _description = 'Voucher Items'
    _rec_name = 'item'

    item = fields.Text()
    price = fields.Float()
