from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class PatientDocuments(models.Model):
    _name = 'syscraft.patient.documents.tbl'
    _description = 'Patient Documents'
    _rec_name = 'patient_name_id'

    patient_name_id = fields.Many2one('syscraft.clinic.tbl', string='Patient Name ')
    patient_age = fields.Integer(compute='fill_age', string='Patient Age', store=True, readonly=False)
    patient_gender = fields.Char(compute='fill_gender', string='Patient Gender', store=True, readonly=False)
    patient_phone = fields.Char(compute='fill_phone', string='Patient Phone', store=True, readonly=False)
    patient_email = fields.Char(compute='fill_email', string='Patient Email', store=True, readonly=False)
    clinic_name = fields.Many2one('syscraft.clinic.records.tbl')
    IMAGE = fields.Image()
    REF_NO = fields.Char()

    def action_add_doc(self):
        print('Button clicked')

    def action_view_doc(self):
        print('Button clicked')

    def action_open_write_letter(self):
        print('Button clicked')

    @api.depends('patient_name_id.AGE')
    def fill_age(self):
        for rec in self:
            try:
                if rec.patient_name_id.AGE:
                    rec.patient_age = rec.patient_name_id.AGE

            except Exception as e:
                _logger.exception("Error in _compute_patient_age: %s", e)

    @api.depends('patient_name_id.GENDER')
    def fill_gender(self):
        for rec in self:
            try:
                if rec.patient_name_id.GENDER:
                    rec.patient_gender = rec.patient_name_id.GENDER

            except Exception as e:
                _logger.exception("Error in _compute_patient_age: %s", e)

    @api.depends('patient_name_id.CONTACT')
    def fill_phone(self):
        for rec in self:
            try:
                if rec.patient_name_id.CONTACT:
                    rec.patient_phone = rec.patient_name_id.CONTACT

            except Exception as e:
                _logger.exception("Error in _compute_patient_age: %s", e)

    @api.depends('patient_name_id.EMAIL')
    def fill_email(self):
        for rec in self:
            try:
                if rec.patient_name_id.EMAIL:
                    rec.patient_email = rec.patient_name_id.EMAIL

            except Exception as e:
                _logger.exception("Error in _compute_patient_age: %s", e)
