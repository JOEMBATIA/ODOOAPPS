from odoo import models, fields, api

class Patient(models.Model):
    _name = 'patient.management'
    _inherit = ['mail.thread']
    _description = 'Patient Management'

    name = fields.Char(string='Patient Name', required=True, tracking=True)
    patient_id = fields.Char(string='Patient ID', required=True, tracking=True)
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True)
    address = fields.Text(string='Address', tracking=True)
    hospital = fields.Char(string='Hospital', tracking=True)
    contact_number = fields.Char(string='Contact Number', tracking=True)
    expenses_ids = fields.One2many('patient.expense', 'patient_id', string='Expenses')
    progress_ids = fields.One2many('patient.progress', 'patient_id', string='Progress')
    progress = fields.Float('Progress')
    date = fields.Date('Date')
