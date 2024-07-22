from odoo import api, fields, models


class MedicalSummary(models.Model):
    _name = 'syscraft.medical.summary'
    _descritption = 'Medical Summary'

    patient_name_id = fields.Many2one('syscraft.clinic.tbl')
    pregnancy = fields.Char()
    total_visits = fields.Char()
    points = fields.Char()
    Due = fields.Float(string='Adv (KSH) ')
    Billed = fields.Float(string='Billed (KSH) ')
    category = fields.Char()
    comments = fields.Char()
    allergy = fields.Char()
    visits = fields.Char()
    family_members = fields.Char()
    next_appt_id = fields.Char(compute='_fill_next_appointment')

    @api.depends('patient_name_id.NEXTAPPT')
    def _fill_next_appointment(self):
        for rec in self:
            if rec.patient_name_id.NEXTAPPT:
                rec.next_appt_id = rec.patient_name_id.NEXTAPPT
            else:
                rec.next_appt_id = 'No appointment yet'

    @api.depends('patient_name_id.NETBALANCE')
    def _fill_net_balance(self):
        for rec in self:
            if rec.patient_name_id.NETBALANCE:
                rec.Due = rec.patient_name_id.NETBALANCE
            else:
                rec.Due = 0.0
