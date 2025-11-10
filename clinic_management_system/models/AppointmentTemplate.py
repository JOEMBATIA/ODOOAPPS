from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from _datetime import datetime


class AppointmentTemplate(models.Model):
    _name = 'syscraft.appointment.template.tbl'
    _description = 'Appointment Template'
    _rec_name = 'ref_number'

    ref_number = fields.Char(string='Reference Number', readonly=True, copy=False,
                             required=True, default=lambda self: _('NEW'))
    appointment_name = fields.Char(string='Appointment Name ')
    appointment_start = fields.Datetime(string='Appointment Start ')
    appointment_end = fields.Datetime(string='Appointment End ')
    appointment_duration = fields.Float(compute='_compute_appointment_duration', store=True)
    # appointment_duration_str = fields.Char(string='Appointment Duration ', compute='_compute_appointment_duration_str',tore=True)
    consultation_service = fields.Selection(
        [('amethyst', 'Amethyst'), ('emarald', 'Emarald'), ('emarald', 'Emarald'), ('haircut', 'Haircut'),
         ('jade', 'Jade'),
         ('moonshine', 'Moonshine'), ('onyx', 'Onyx'), ('perl', 'Perl'), ('rose quartz', 'Rose Quartz'),
         ('selentine', 'Selentine')],
        string="Resources ")
    urgent = fields.Boolean()
    resource_id = fields.Many2one('syscraft.resources.tbl', string='Resource')
    appointment_color = fields.Char(string='Appointment color')

    @api.model
    def create(self, vals):
        if 'ref_number' not in vals or vals['ref_number'] == _('NEW'):
            sequence_value = self.env['ir.sequence'].next_by_code('appointment.temp') or _('NEW')
            vals['ref_number'] = sequence_value

        return super(AppointmentTemplate, self).create(vals)

    @api.constrains('appointment_start', 'appointment_end')
    def _appointment_validation(self):
        for rec in self:
            if rec.appointment_end < rec.appointment_start:
                raise ValidationError(
                    "Appointment end-date is back date, you have set the appointment end date before the start")
            if rec.appointment_end == rec.appointment_start:
                raise ValidationError(
                    "Appointment duration is null, you have set the duration of the appointment to a zero value")
            if rec.appointment_start < datetime.now():
                raise ValidationError("Appointment start date is backdated ")

    @api.depends('appointment_start', 'appointment_end')
    def _compute_appointment_duration(self):
        for rec in self:
            if rec.appointment_start and rec.appointment_end:
                print('Computing the appointment duration ...')
                duration = rec.appointment_end - rec.appointment_start
                minutes = duration.total_seconds() / 60
                rec.appointment_duration = minutes
            else:
                rec.appointment_duration = 0.0
                print('Computation finished successfully')

    # @api.depends('appointment_duration')
    # def _compute_appointment_duration_str(self):
    #     for rec in self:
    #         print('Validating nonNull attributes ....')
    #
    #         if rec.appointment_duration is not False:
    #             rec.appointment_duration_str = f"{rec.appointment_duration} minutes"
    #         else:
    #             rec.appointment_duration_str = ""
