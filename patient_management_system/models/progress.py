from odoo import models, fields, api

class PatientProgress(models.Model):
    _name = 'patient.progress'
    _description = 'Patient Progress'

    patient_id = fields.Many2one('patient.management', string='Patient', required=True, ondelete='cascade')
    date = fields.Date(string='Date', required=True)
    description = fields.Text(string='Progress Notes')
    status = fields.Selection([('stable', 'Stable'), ('critical', 'Critical'), ('recovering', 'Recovering')], string='Status')
