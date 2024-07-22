from odoo import fields, models, api


class Documents(models.Model):
    # defines the table name inside the database
    _name = "syscraft.clinic.documents.tbl"
    _inherit = "mail.thread"
    _description = "Documents"

    DATE = fields.Date(string="Date ")
    PHONE = fields.Char(string="Phone ")
    EMAIL = fields.Char(string="Email ")
    DOC_DETAILS = fields.Text(string="Document Details ")
    CONTACT = fields.Date(string="Contact Name ")
    CONTACT_PHONE = fields.Date(string="Contact Phone ")
    CONTACT_EMAIL = fields.Date(string="Contact Email ")
    CREATED_BY = fields.Text(string="Created by ")
    SIGNED_BY = fields.Text(string="Signed by ")
    REF_NO = fields.Char(string="")
