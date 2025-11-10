from _datetime import datetime

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Patient(models.Model):
    # defines the table name inside the database
    _name = "syscraft.clinic.tbl"
    _inherit = "mail.thread"
    _description = "Patient records"
    _rec_name = "NAME"

    # defining fields ie columns in the table
    NAME = fields.Char(String="Name", required=True, tracking=True)
    ADDRESS1 = fields.Char(String="Address1", tracking=True)
    ADDRESS2 = fields.Char(String="Address2", tracking=True)
    ADDRESS3 = fields.Char(String="Address3", tracking=True)
    IMAGE = fields.Image(String="", tracking=True)
    CITY = fields.Char(String="Address3", tracking=True)
    POST_CODE = fields.Char(String="Address3", tracking=True)
    STATE1 = fields.Char(String="Address3", tracking=True)
    REF_NO = fields.Text(String="Reference No", tracking=True)
    AVANE = fields.Selection(
        [('scheduled', 'Scheduled'), ('waiting', 'Waiting'), ('confirmed', 'Confirmed'), ('engaged', 'Engaged'),
         ('check out', 'Check Out'), ('cancelled', 'Cancelled')], string="Appointment Status")
    COUNTRY = fields.Selection([('Nigeria', 'Nigeria'), ('Kenya', 'Kenya'), ('ALGERIA', 'ALGERIA'),
                                ('ALGERIA', 'ALGERIA'), ('AFGHANISTAN', 'AFGHANISTAN'), ('ANDORRA', 'ANDORRA'),
                                ('BULGARIA', 'BULGARIA'), ('BOTSWANA', 'BOTSWANA')], String="Country")
    CONTACT = fields.Text(String="Phone Number", tracking=True)
    NETBALANCE = fields.Char(String="Net balance", tracking=True)
    NEXTAPPT = fields.Datetime(String="Appointment start", tracking=True)
    APPT_ID = fields.Many2one('syscraft.clinic.tbl', String="Appointments", tracking=True)
    APPT_COUNT = fields.Integer(string="Appointment count ", compute="compute_appointment_count", store=True)
    APPT_FIN = fields.Datetime(String="Appointment end", tracking=True)
    APPT_DURATION = fields.Integer(String="Appointment Duration(Minutes) ", compute="_compute_appointment_duration",
                                   store=True)
    DOB = fields.Date(String="Date of birth ", tracking=True)
    CLINIC_NAME = fields.Many2one('syscraft.clinic.records.tbl', string="Clinic name ")
    GENDER = fields.Selection([('male', 'Male'), ('female', 'Female')], String="Gender")
    CATEGORY_NAME = fields.Many2many('syscraft.category.tbl', String="Service ")
    NOTES = fields.Char(String="Notes", tracking=True)
    EMAIL = fields.Text(String="Email address ", tracking=True)
    PHYSICIAN = fields.Many2one('syscraft.physicians.tbl', string="Physician/Practitioner ")
    IsChild = fields.Boolean(String="Is Child", tracking=True)
    AGE = fields.Integer(String="Age", compute="_compute_age", store=True)
    RESOURCE = fields.Selection([('amethyst', 'Amethyst'), ('emarald', 'Emarald'), ('emarald', 'Emarald'), ('haircut', 'Haircut'), ('jade', 'Jade'),
                                 ('moonshine', 'Moonshine'), ('onyx', 'Onyx'), ('perl', 'Perl'), ('rose quartz', 'Rose Quartz'), ('selentine', 'Selentine')],
                                string="Resources ")
    resource_id = fields.Many2one('syscraft.resources.tbl', string='Resource')
    MED_SUMMARY = fields.Text(string="Medical summary")
    attachment = fields.Binary(string='Attachment ', attachment=True)
    attachment_filename = fields.Char(string='Attachment filename')
    file_category = fields.Many2one('syscraft.file.category.tbl')

    @api.model_create_multi
    def _create(self, vals_list):
        for vals in vals_list:
            existing_patients = self.env['syscraft.clinic.tbl'].search([('NAME', '=', vals.get('NAME'))])
            if existing_patients:
                raise ValidationError("Patient with the same name already exists")
        return super(Patient, self)._create(vals_list)

    def compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['syscraft.clinic.tbl'].search_count([('NAME', '=', rec.NAME)])
            rec.NAME = appointment_count

    def action_open_appoinment(self):
        print('Button clicked ...')

    @api.onchange('AGE')
    def _onchange_age(self):
        if self.AGE <= 5 and self.AGE == 0:
            self.IsChild = True
        else:
            self.IsChild = False

    @api.constrains('APPT_FIN', 'NEXTAPPT')
    def _appointment_validation(self):
        for rec in self:
            if rec.APPT_FIN < rec.NEXTAPPT:
                raise ValidationError(
                    "Appointment end-date is back date, you have set the appointment end date before the start")
            if rec.APPT_FIN == rec.NEXTAPPT:
                raise ValidationError(
                    "Appointment duration is null, you have set the duration of the appointment to a zero value")
            if rec.NEXTAPPT < datetime.now():
                raise ValidationError("Appointment start date is backdated ")

    @api.depends('APPT_FIN', 'NEXTAPPT')
    def _compute_appointment_duration(self):
        for rec in self:
            if rec.APPT_FIN and rec.NEXTAPPT:
                duration = rec.APPT_FIN - rec.NEXTAPPT
                minutes = duration.total_seconds() / 60
                rec.APPT_DURATION = minutes

    @api.depends('DOB')
    def _compute_age(self):
        for rec in self:
            current_date = fields.Date.today()
            age = 0  # Initialize age to 0
            if rec.DOB:
                age = current_date.year - rec.DOB.year
                if (current_date.month, current_date.day) < (rec.DOB.month, rec.DOB.day):
                    raise ValidationError("Invalid Year of birth")
            rec.AGE = age

    class Physician(models.Model):
        _name = "syscraft.physicians.tbl"
        _description = "Physicians.model"

        PHYSICIAN_NAME = fields.Text(string="Physician Name ")
        PHONE = fields.Text(string="Phone No. ")
        EMAIL = fields.Text(string="Email address ")

        def name_get(self):
            result = []
            for rec in self:
                physician_name = rec.PHYSICIAN_NAME or ""
                phone_str = str(rec.PHONE) if rec.PHONE else ""
                name = f"[{physician_name}] {phone_str}"
                result.append((rec.id, name))
            return result

    class Category(models.Model):
        _name = "syscraft.category.tbl"
        _description = "Categories"
        _rec_name = "CATEGORY_NAME"

        CATEGORY_NAME = fields.Char(string="Service ")

    class Resources(models.Model):
        _name = "syscraft.resources.tbl"
        _description = "Resoources"
        _rec_name = "name"

        name = fields.Char(string="Resource Name ")

    class FileCategory(models.Model):
        _name = "syscraft.file.category.tbl"
        _description = "File Categories"
        _rec_name = "name"

        name = fields.Char(string="Set a Category for the File ")
