from odoo import fields, models, api, _
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class Pharmacy(models.Model):
    # defines the table name inside the database
    _name = "syscraft.clinic.pharmacy.tbl"
    _inherit = "mail.thread"
    _description = "Pharmacy records"
    _rec_name = 'patient_name_id'

    # defining fields ie columns in the table
    STATUS_SYS = fields.Selection([('Pending', 'Pending'), ('Dispensed', 'Dispensed')]
                                  , String="Status", required=True, tracking=True)
    PATIENT_DETAILS = fields.Char(String="Patient details", tracking=True)
    PATIENT_EMAIL = fields.Char(String="Patient details", tracking=True)
    PATIENT_PHONE = fields.Char(String="Patient details", tracking=True)
    CONTACT_DETAILS = fields.Char(String="Contact", tracking=True)
    CONTACT_NAME = fields.Char(String="Contact", tracking=True)
    CONTACT_PHONE = fields.Char(String="Contact", tracking=True)
    CONTACT_EMAIL = fields.Char(String="Contact", tracking=True)
    AGE = fields.Integer(String="Age", tracking=True)
    GENDER = fields.Selection([('male', 'Male'), ('female', 'Female')], String="Gender")
    PHYSICIAN_id = fields.Many2one('syscraft.physicians.tbl', string="Physician/Practitioner Mobile ")
    NAME = fields.Char(String="Name/Mobile No/File No", tracking=True)
    REF_NO = fields.Integer(String="Ref No", tracking=True)
    PRESC_START = fields.Date(String="Prescription Start ", tracking=True)
    PRESC_END = fields.Date(String="Prescription end", tracking=True)
    pharmacy_item_ids = fields.One2many('syscraft.pharmacy.bill.items.tbl', 'pharmacy_id', tracking=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done'), ('cancelled', 'Cancelled')], default="draft",
        string="State")
    location = fields.Many2one('syscraft.clinic.records.tbl', string="Clinic Name ")
    patient_name_id = fields.Many2one('syscraft.clinic.tbl', string="Patient Name ")
    PAYMENT_MODE = fields.Selection(
        [('Bad debts', 'Bad debts'), ('Card payment', 'Card payment'), ('Euro Bank', 'Euro Bank'),
         ('Euro Cash', 'Euro Cash'), ('Insurance', 'Insurance'), ('Mpesa', 'Mpesa'),
         ('Staff Discount', 'Staff Discount'), ('USD Bank', 'USD Bank'), ('USD Cash', 'USD Cash'),
         ('Cheque', 'Cheque'), ('off', 'off'), ('Online payment', 'Online payment'),
         ('Net Banking', 'Net Banking'),
         ('Mpesa', 'Mpesa')], String="Payment Mode ")
    note = fields.Html(string="Terms and conditions", translate=True)
    invoice_date = datetime.now().strftime('%Y-%m-%d')
    invoice_date_due = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

    def action_open_patient(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'syscraft.clinic.tbl',  # Replace with your actual patient model
            'view_mode': 'form',
            'view_id': self.env.ref('clinic_management_system.view_patient_form').id,
            # Replace with your actual view ID
            'target': 'current',
            'res_id': self.patient_name_id.id,  # Replace with the field containing patient ID
        }

    def action_send_email(self):
        template = self.env.ref('clinic_management_system.prescription_email_template')
        email_values = {'subject': 'Prescription and Invoice Details'}

        for rec in self:
            if template.send_mail(rec.id, force_send=True, email_values=email_values):
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'param': {
                        'message': _('Email sent successfully'),
                        'type': 'success',
                        'sticky': False
                    }
                }
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'param': {
                        'message': _('Email not sent'),
                        'type': 'danger',
                        'sticky': False
                    }
                }

    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'done':
            self.STATUS_SYS = 'Dispensed'
        else:
            self.STATUS_SYS = 'Pending'

    class PharmacyBillItems(models.Model):
        _name = "syscraft.pharmacy.bill.items.tbl"
        _description = "Pharmacy Items"

        item_id = fields.Many2one('syscraft.product.tbl', string="Item ")
        price = fields.Float(string="Price ")
        quantity = fields.Integer(string="QTY ", default=1.0, readonly=False)
        discount = fields.Integer(string="Discount(%) ")
        total = fields.Float(string="Item Total ", compute="compute_total", readonly=True)
        pharmacy_id = fields.Many2one('syscraft.clinic.pharmacy.tbl')
        note = fields.Html(string="Terms and conditions", translate=True)

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
