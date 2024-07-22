from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class Package(models.Model):
    # defines the table name inside the database
    _name = "syscraft.clinic.financials.package.tbl"
    _inherit = "mail.thread"
    _description = "Package records"
    _rec_name = "PATIENT_id"

    # defining fields ie columns in the table
    NEW = fields.Char(string="New", default="NEW")
    active = fields.Boolean(default=True)
    PATIENT_id = fields.Many2one('syscraft.clinic.tbl', string="Patient Name")
    HEADS = fields.Selection([('Heads', 'Heads'), ('Expense:Stock', 'Expense:Stock')], String="Heads")
    TYPE = fields.Selection([('Income', 'Income'), ('Expense', 'Expense')], String="Type")
    LOCATION = fields.Selection([('Avane Dermatology Clinic, Girigiri(G)', 'Avane Dermatology Clinic, Girigiri(G)'),
                                 ('Avane Dermatology Clinic, Girigiri(USD)(USG)',
                                  'Avane Dermatology Clinic, Girigiri(USD)(USG)'),
                                 ('Avane Dermatology Clinic, Park Suites(P)',
                                  'Avane Dermatology Clinic, Park Suites(P)'),
                                 ('Avane Dermatology Clinic, Park Suites(USD)(USG)',
                                  'Avane Dermatology Clinic, Park Suites(USD)(USG)'),
                                 ('Avane Dermatology Clinic, Yaya (Y)', 'Avane Dermatology Clinic, Yaya (Y)'),
                                 ('Avane Dermatology Clinic, Yaya (USD)(USG)',
                                  'Avane Dermatology Clinic, Yaya (USD)(USG)'),
                                 ('Avane SPA, (SPA)', 'Avane SPA, (SPA)'),
                                 ('Avane SPA, (USD)(USG)', 'Avane SPA, (USD)(USG)'),
                                 ('Avane Store, (AVS)', 'Avane Store, (AVS)')],
                                String="Type")
    EXPENSE_DATE = fields.Date(String="Expense Date")
    EXPENSE_DUE_DATE = fields.Date(String="Expense Due Date")
    PAYMENT_DATE = fields.Date(String="Payment Date")
    VOUCHER_DATE = fields.Date(String="Voucher Date")
    PAYMENT_MODE = fields.Selection(
        [('Bad debts', 'Bad debts'), ('Card payment', 'Card payment'), ('Euro Bank', 'Euro Bank'),
         ('Euro Cash', 'Euro Cash'), ('Insurance', 'Insurance'), ('Mpesa', 'Mpesa'),
         ('Staff Discount', 'Staff Discount'), ('USD Bank', 'USD Bank'), ('USD Cash', 'USD Cash'),
         ('Cheque', 'Cheque'), ('off', 'off'), ('Online payment', 'Online payment'),
         ('Net Banking', 'Net Banking'),
         ('Mpesa', 'Mpesa')], String="Payment state")
    PAYMENT_STATE = fields.Selection([('paid & unpaid', 'paid & unpaid'), ('paid', 'paid'),
                                      ('unpaid', 'unpaid')], String="Payment")
    VOUCHER_DETAILS = fields.Text(String="Voucher Details", tracking=True)
    NOTES = fields.Text(String="Notes ", tracking=True)
    VOUCHER_TYPE = fields.Text(String="Voucher type", tracking=True)
    AMOUNT = fields.Text(String="Amount", tracking=True)
    GENDER = fields.Selection([('male', 'Male'), ('female', 'Female')], String="Gender", tracking=True)
    BELONGSTOCLINIC = fields.Selection(
        [('Avane Dermatology Clinic, Girigiri(G)', 'Avane Dermatology Clinic, Girigiri(G)'),
         ('Avane Dermatology Clinic, Girigiri(USD)(USG)',
          'Avane Dermatology Clinic, Girigiri(USD)(USG)'),
         ('Avane Dermatology Clinic, Park Suites(P)',
          'Avane Dermatology Clinic, Park Suites(P)'),
         ('Avane Dermatology Clinic, Park Suites(USD)(USG)',
          'Avane Dermatology Clinic, Park Suites(USD)(USG)'),
         ('Avane Dermatology Clinic, Yaya (Y)', 'Avane Dermatology Clinic, Yaya (Y)'),
         ('Avane Dermatology Clinic, Yaya (USD)(USG)', 'Avane Dermatology Clinic, Yaya (USD)(USG)'),
         ('Avane SPA, (SPA)', 'Avane SPA, (SPA)'),
         ('Avane SPA, (USD)(USG)', 'Avane SPA, (USD)(USG)'),
         ('Avane Store, (AVS)', 'Avane Store, (AVS)')],
        String="Clinic name", tracking=True)
    NEXTAPPT = fields.Date(String="Appointment start", tracking=True)
    note = fields.Html(string="Terms and conditions", translate=True)
    PHONE = fields.Char(String="Phone ", tracking=True)
    EMAIL = fields.Char(String="Email ", tracking=True)
    TOTAL = fields.Integer(String="Amount Inclusive of taxes ", tracking=True)
    REF_NO = fields.Integer(String="Reference No ", tracking=True)
    STATE = fields.Selection([('draft', 'draft'), ('confirm', 'confirm'), ('done', 'done')], String="")
    NETBALANCE = fields.Char(String="Net balance", tracking=True)
    START_PERIOD = fields.Date(String="Start period ", tracking=True)
    END_PERIOD = fields.Date(String="End period ", tracking=True)
    QUANTITY = fields.Integer(String="Quantity ", tracking=True)
    order_line_ids = fields.One2many('syscraft.package.lines.tbl', 'package_id')
    product_id = fields.Many2one('syscraft.inventory.tbl', string="Items ")

    def action_open_patient(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'syscraft.clinic.tbl',  # Replace with your actual patient model
            'view_mode': 'form',
            'view_id': self.env.ref('SyscraftClinicManagement.view_patient_form').id,
            # Replace with your actual view ID
            'target': 'current',
            'res_id': self.PATIENT_id.id,  # Replace with the field containing patient ID
        }


class PackageLine(models.Model):
    _name = "syscraft.package.lines.tbl"
    _description = "Package Lines"

    item_id = fields.Many2one('syscraft.product.tbl', string="Item ")
    price = fields.Float(string="Price ")
    quantity = fields.Integer(string="QTY ", default=1.0, readonly=False)
    discount = fields.Integer(string="Discount(%) ")
    total = fields.Float(string="Item Total ", compute="compute_total", readonly=True)
    package_id = fields.Many2one('syscraft.clinic.financials.package.tbl')

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

    @api.onchange('item_id')
    def fill_price_field(self):
        if self.item_id:
            self.price = self.item_id.price


class Items(models.Model):
    _name = "syscraft.financials.items.tbl"
    _description = "Items"

    ITEMS = fields.Char(string="Item ")
