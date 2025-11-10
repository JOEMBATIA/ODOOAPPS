from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)


class Library(models.Model):
    _name = 'syscraft.library.tbl'
    _description = 'Library'
    _rec_name = 'date'

    date = fields.Date(string='Date ')
    doc_name = fields.Char(string='Document Name ')
    doc_created_date = fields.Date(string='Document Created Date ')
    created_by = fields.Char(string='Created By')
    clinic = fields.Many2one('syscraft.clinic.records.tbl')
    signed_by = fields.Char(string='Signed By')
    doc_details = fields.Char(string='Document Details ',
                              compute='_compute_combined_doc_fields')
    patient_details = fields.Char(string='Patient Details',
                                  compute='_compute_combined_patient_details')
    created_and_clinic = fields.Char(string='Created by & Clinic ',
                                     compute='_compute_combined_created_and_clinic_fields')
    attachment = fields.Binary(string='Attachment ', attachment=True)
    file_category = fields.Many2one('syscraft.file.category.tbl')
    attachment_filename = fields.Char(string='Attachment filename')

    @api.depends('doc_name', 'doc_created_date')
    def _compute_combined_doc_fields(self):
        for record in self:
            record.doc_details = f"{record.doc_name} | {record.doc_created_date}"

    @api.depends('created_by', 'clinic')
    def _compute_combined_created_and_clinic_fields(self):
        for record in self:
            record.created_and_clinic = f"{record.created_by} | {record.clinic.BELONGSTOCLINIC}"
