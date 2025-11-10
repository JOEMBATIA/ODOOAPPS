from odoo import models, fields, api

class PatientExpense(models.Model):
    _name = 'patient.expense'
    _description = 'Patient Expenses'

    patient_id = fields.Many2one('patient.management', string='Patient', required=True, ondelete='cascade')
    date = fields.Date(string='Expense Date', required=True)
    description = fields.Char(string='Description')
    amount = fields.Float(string='Amount')
