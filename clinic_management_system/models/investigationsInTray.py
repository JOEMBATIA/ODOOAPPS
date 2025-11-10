from odoo import fields, models, api


class InvestigationsInTray(models.Model):
    # defines the table name inside the database
    _name = "syscraft.clinic.investigations.in.tray.tbl"
    _inherit = "mail.thread"
    _description = "Invesigations In Tray records"

    # defining fields ie columns in the table
    PATIENT = fields.Many2one('syscraft.clinic.tbl', String="Patient/Ref No/Mobile/File No", required=True, tracking=True)
    PHYSICIAN_id = fields.Many2one('syscraft.physicians.tbl', string="Physician/Practinioner ")
    INVESTIGATION = fields.Char(String="Investigation", tracking=True)
    CATEGORIES = fields.Selection([('lab', 'lab'), ('radiologist', 'radiologists')], String="All Catgories")
    TYPE = fields.Selection([('my', 'my'), ('All investigations', 'All investigations')], String="Type")
    DATE = fields.Date(String="Date")
    END_DATE = fields.Date(String="Date")
    CLINIC = fields.Many2one('syscraft.clinic.records.tbl', string='Clinic Name')
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancelled', 'Cancelled')], default="draft",
        string="Status")
    OTHER = fields.Text(string="Other info ")
    NOTES = fields.Text(string="Notes ")
    IMAGE = fields.Image(String="", tracking=True)
    REF_NO = fields.Char()
