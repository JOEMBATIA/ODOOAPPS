from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)


class PaperWork(models.Model):
    _name = 'syscraft.paper.work.tbl'
    _description = 'Paper Work'
    _rec_name = 'patient_name_id'

    date = fields.Datetime(string='Paper Work Created On ')
    doc_name = fields.Char(string='Paper Work Name ', compute='fill_paper_work_name',
                           store=True)
    patient_name_id = fields.Many2one('syscraft.clinic.tbl', string='Patient Name')
    patient_phone = fields.Char(compute='fill_phone', string='Patient Phone',
                                store=True, readonly=True)
    patient_email = fields.Char(compute='fill_email', string='Patient Email',
                                store=True, readonly=True)
    created_by = fields.Char(string='Created By')
    clinic = fields.Many2one('syscraft.clinic.records.tbl')
    paper_work_details = fields.Char(string='Document Details ',
                                     compute='_compute_combined_doc_fields')
    patient_details = fields.Char(string='Patient Details',
                                  compute='_compute_combined_patient_details')
    created_and_clinic = fields.Char(string='Created by & Clinic ',
                                     compute='_compute_combined_created_and_clinic_fields')
    paper_work_to_add = fields.Many2one('syscraft.paper.work.type.tbl', string="Select the paperwork you want to add ")

    @api.depends('doc_name', 'date')
    def _compute_combined_doc_fields(self):
        for record in self:
            record.paper_work_details = f"{record.doc_name} | {record.date}"

    @api.depends('patient_name_id', 'patient_phone', 'patient_email')
    def _compute_combined_patient_details(self):
        for record in self:
            record.patient_details = (f"{record.patient_name_id.NAME} | {record.patient_phone}"
                                      f" | {record.patient_email}")

    @api.depends('created_by', 'clinic')
    def _compute_combined_created_and_clinic_fields(self):
        for record in self:
            record.created_and_clinic = f"{record.created_by} | {record.clinic.BELONGSTOCLINIC}"

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

    @api.depends('paper_work_to_add.name')
    def fill_paper_work_name(self):
        for rec in self:
            try:
                if rec.paper_work_to_add.name:
                    rec.doc_name = rec.paper_work_to_add.name

            except Exception as e:
                _logger.exception("Error in _compute_patient_age: %s", e)

    class PaperWorkType(models.Model):
        _name = 'syscraft.paper.work.type.tbl'
        _description = 'Paper Work Type'

        name = fields.Char(string='Paper Work Name')
