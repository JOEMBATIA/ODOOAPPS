from odoo import fields, models, api


class Refund(models.Model):
    # defines the table name inside the database
    _name = "syscraft.clinic.financials.refund.tbl"
    _inherit = "mail.thread"
    _description = "Refund records"
    _rec_name = "PATIENT_id"

    # defining fields ie columns in the table
    active = fields.Boolean(default=True)
    PATIENT_id = fields.Many2one('syscraft.clinic.tbl', string="Patient Name")
    TYPE = fields.Selection([('Income', 'Income'), ('Expense', 'Expense')], String="Type")
    PAYMENT_DATE = fields.Date(String="Payment Date")
    AMOUNT = fields.Float(String="Refund Amount")
    PAYMENT_MODE = fields.Selection(
        [('Bad debts', 'Bad debts'), ('Card payment', 'Card payment'), ('Euro Bank', 'Euro Bank'),
         ('Euro Cash', 'Euro Cash'), ('Insurance', 'Insurance'), ('Mpesa', 'Mpesa'),
         ('Staff Discount', 'Staff Discount'), ('USD Bank', 'USD Bank'), ('USD Cash', 'USD Cash'),
         ('Cheque', 'Cheque'), ('off', 'off'), ('Online payment', 'Online payment'),
         ('Net Banking', 'Net Banking'),
         ('Mpesa', 'Mpesa')], String="Payment Mode")
    NOTES = fields.Text(String="Notes ", tracking=True)
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
    PHONE = fields.Char(String="Phone ", tracking=True)
    EMAIL = fields.Char(String="Email ", tracking=True)
    REF_NO = fields.Integer(String="Reference No ", tracking=True)
    STATE = fields.Selection([('draft', 'draft'), ('confirm', 'confirm'), ('done', 'done')], String="")
    NETBALANCE = fields.Char(String="Net balance", tracking=True)
    START_PERIOD = fields.Date(String="Start period ", tracking=True)
    END_PERIOD = fields.Date(String="End period ", tracking=True)
    QUANTITY = fields.Integer(String="Quantity ", tracking=True)
    AGE = fields.Integer(String="Age ", tracking=True)
    product_id = fields.Many2one('syscraft.inventory.tbl', string="Items ")
    category_id = fields.Many2one('syscraft.category.tbl', string="Category ")

