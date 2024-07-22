from odoo import fields, models, api


class Expense(models.Model):
    # defines the table name inside the database
    _name = "syscraft.clinic.financials.expense.tbl"
    _inherit = "mail.thread"
    _description = "Expense records"

    # defining fields ie columns in the table
    active = fields.Boolean(default=True)
    HEADS = fields.Selection([('Heads', 'Heads'), ('Expense:Stock', 'Expense:Stock')], String="Heads")
    TYPE = fields.Selection([('Income', 'Income'), ('Expense', 'Expense')], String="Type")
    EXPENSE_DATE = fields.Date(String="Expense Date")
    EXPENSE_DUE_DATE = fields.Date(String="Expense Due Date")
    PAYMENT_DATE = fields.Date(String="Payment Date")
    VOUCHER_DATE = fields.Date(String="Voucher Date")
    EXPENSE_TYPE = fields.Selection([('expense', 'Expense'), ('income', 'Income')], String="Type ")
    PAYMENT_MODE = fields.Selection(
        [('Bad debts', 'Bad debts'), ('Card payment', 'Card payment'), ('Euro Bank', 'Euro Bank'),
         ('Euro Cash', 'Euro Cash'), ('Insurance', 'Insurance'), ('Mpesa', 'Mpesa'),
         ('Staff Discount', 'Staff Discount'), ('USD Bank', 'USD Bank'), ('USD Cash', 'USD Cash'),
         ('Cheque', 'Cheque'), ('off', 'off'), ('Online payment', 'Online payment'),
         ('Net Banking', 'Net Banking'),
         ('Mpesa', 'Mpesa')], String="Payment state")
    VOUCHER_DETAILS = fields.Char(String="Voucher Details", tracking=True)
    NOTES = fields.Text(String="Notes ", tracking=True)
    VOUCHER_TYPE = fields.Char(String="Voucher type", tracking=True)
    AMOUNT = fields.Float(String="Amount(incl. TAX) ", tracking=True)
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
    note = fields.Html(string="Terms and conditions", translate=True)
    NETBALANCE = fields.Char(String="Net balance", tracking=True)
    START_PERIOD = fields.Date(String="Start period ", tracking=True)
    END_PERIOD = fields.Date(String="End period ", tracking=True)
    VENDOR_id = fields.Many2one('syscraft.expense.vendor.tbl', String="Vendor ", tracking=True)
    SERVICE_id = fields.Many2one('syscraft.expense.service.category.tbl', String="Link to service category ", tracking=True)
    CATEGORY_id = fields.Many2one('syscraft.category.tbl', String="Link to product category ", tracking=True)
    ref_no = fields.Text()

    class Vendor(models.Model):
        _name = "syscraft.expense.vendor.tbl"
        _description = "Vendor Details"

        phone = fields.Integer(string="Phone ", required=True)
        vendor_name = fields.Char(string="Phone ")
        email = fields.Char(string="Email ")

    class ServiceCatgeory(models.Model):
        _name = "syscraft.expense.service.category.tbl"
        _description = "Service Details"

        service = fields.Char()
