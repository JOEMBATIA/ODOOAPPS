import html2text
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from jinja2 import Environment, BaseLoader
import socket
import logging
from datetime import datetime


from odoo.http import request

_logger = logging.getLogger(__name__)


class Volunteer(models.Model):
    _name = 'volunteer.volunteer'
    _description = 'Volunteer'
    _rec_name = 'name'
    _inherit = ['mail.thread',
                'mail.activity.mixin']  # adds the necessary functionality for the chatter and activity tracking.

    lang = fields.Char("Language", tracking=True, default='En', readonly=True)
    reference = fields.Char(string='Reference', readonly=True)
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    status = fields.Selection(
        [('rejected', 'Rejected'), ('to be approved', 'To be Approved'), ('approved', 'Approved')],
        string="Application Status", default="to be approved", tracking=True)
    payment_status = fields.Selection([('paid', 'Paid'), ('not paid', 'Not Paid'), ('to be paid', 'To Be Paid')], tracking=True)
    project_ids = fields.Many2many('project.project', string='Projects', tracking=True)
    image = fields.Image()
    phone = fields.Char(string='Phone', tracking=True)
    address = fields.Char(string='Address', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender',
                              tracking=True)
    country_id = fields.Many2one('res.country')
    state_id = fields.Many2one('res.country.state', domain="[('country_id', '=?', country_id)]", string='City/State',
                               tracking=True)
    mode = fields.Selection([('onsite', 'Onsite'), ('remote', 'Remote/Online'), ('hybrid', 'Hybrid')], tracking=True)
    identification = fields.Char(string='Passport/National ID', tracking=True)
    message = fields.Text(string='Reason you are joining us', tracking=True)
    hobbies = fields.Text(string='What are your hobbies', tracking=True)
    emergency_name = fields.Char(string='Emergency Contact Name', tracking=True)
    emergency_phone = fields.Char(string='Emergency Phone', tracking=True)
    emergency_relationship = fields.Char(string='Relation', tracking=True)
    emergency_details = fields.Text(string='Condition/allergies', tracking=True)
    area_of_interest = fields.Text(string='Area of interest', tracking=True)
    rejection_reason = fields.Text(string='Rejection Reason')
    signup_url = fields.Char(compute='_compute_signup_url', tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    start_date = fields.Date(string='Volunteering Start Date', tracking=True)
    end_date = fields.Date(string='Volunteering End Date', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=False)
    AFRICAN_COUNTRIES = [
        'DZ', 'AO', 'BJ', 'BW', 'BF', 'BI', 'CM', 'CV', 'CF', 'TD', 'KM', 'CG', 'CD', 'CI', 'DJ', 'EG',
        'GQ', 'ER', 'ET', 'GA', 'GM', 'GH', 'GN', 'GW', 'KE', 'LS', 'LR', 'LY', 'MG', 'MW', 'ML', 'MR',
        'MU', 'MA', 'MZ', 'NA', 'NE', 'NG', 'RW', 'ST', 'SN', 'SC', 'SL', 'SO', 'ZA', 'SS', 'SD', 'SZ',
        'TZ', 'TG', 'TN', 'UG', 'ZM', 'ZW'
    ]

    def _is_african_country(self):
        """Check if the selected country is in Africa"""
        if self.country_id and self.country_id.code in self.AFRICAN_COUNTRIES:
            return True
        return False

    state = fields.Selection([
        ('to be approved', 'To Be Approved'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='to be approved')

    def multiple_action_approve(self):
        for record in self:
            record.status = 'approved'

    def multiple_action_reject(self):
        for record in self:
            record.status = 'rejected'

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date:
                start_date = fields.Date.from_string(record.start_date)
                end_date = fields.Date.from_string(record.end_date)

                delta = (end_date - start_date).days
                if delta < 0:
                    _logger.info("End End Date must be after Start Date. ")
                    raise ValidationError("The volunteering period must be at least one day.")

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                birth_date = fields.Date.from_string(record.date_of_birth)
                today = datetime.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.age = age
            else:
                record.age = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            _logger.info("Before setting reference: %s", vals.get('reference'))
            if not vals.get('reference') or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('volunteer.info') or 'New'
            _logger.info("After setting reference: %s", vals['reference'])

            # Check if country is African and auto-reject silently
            if vals.get('country_id'):
                country = self.env['res.country'].browse(vals['country_id'])
                if country.code in self.AFRICAN_COUNTRIES:
                    vals['status'] = 'rejected'
                    vals['rejection_reason'] = 'Application automatically rejected due to geographical restrictions. The volunteer comes from ' + country.name
                else:
                    vals['status'] = 'to be approved'

        return super(Volunteer, self).create(vals_list)

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f'[{rec.reference}]-{rec.name}'

    def _get_signup_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/web/login"

    def _compute_signup_url(self):
        for record in self:
            record.signup_url = record._get_signup_url()

    def action_approve(self):
        self.status = 'approved'
        # Load the email template
        template = self.env.ref('volunteer_management.volunteer_approval_email_template')

        if template:
            # Send the email using the template
            template.send_mail(self.id, force_send=True)

            # Render the HTML body from the template
            rendered_html_body = self.env['mail.render.mixin'].with_context({})._render_template(
                template.body_html, 'volunteer.volunteer', self.ids
            )[self.id]

            # Convert HTML to plain text
            h = html2text.HTML2Text()
            h.ignore_links = False  # Set to True if you do not want to keep links in the text
            plain_text_body = h.handle(rendered_html_body)

            # Post the plain text message to the Chatter
            self.message_post(
                body=plain_text_body,
                subject=template.subject,
                message_type='notification',
                subtype_xmlid="mail.mt_note"
            )

    def action_reject(self):
        self.status = 'rejected'
        # Load the email template
        template = self.env.ref('volunteer_management.volunteer_rejection_email_template')

        if template:
            # Send the email using the template
            template.send_mail(self.id, force_send=True)

            # Render the HTML body from the template
            rendered_html_body = self.env['mail.render.mixin'].with_context({})._render_template(
                template.body_html, 'volunteer.volunteer', self.ids
            )[self.id]

            # Convert HTML to plain text
            h = html2text.HTML2Text()
            h.ignore_links = False  # Set to True if you do not want to keep links in the text
            plain_text_body = h.handle(rendered_html_body)

            # Post the plain text message to the Chatter
            self.message_post(
                body=plain_text_body,
                subject=template.subject,
                message_type='notification',
                subtype_xmlid="mail.mt_note"
            )

    def action_send_mail(self):
        self.status = 'approved'
        # Load the email template
        template = self.env.ref('volunteer_management.volunteer_approval_email_template')

        if template:
            # Send the email using the template
            template.send_mail(self.id, force_send=True)

            # Render the HTML body from the template
            rendered_html_body = self.env['mail.render.mixin'].with_context({})._render_template(
                template.body_html, 'volunteer.volunteer', self.ids
            )[self.id]

            # Convert HTML to plain text
            h = html2text.HTML2Text()
            h.ignore_links = False  # Set to True if you do not want to keep links in the text
            plain_text_body = h.handle(rendered_html_body)

            # Post the plain text message to the Chatter
            self.message_post(
                body=plain_text_body,
                subject=template.subject,
                message_type='notification',  # or 'comment' depending on your needs
                subtype_xmlid="mail.mt_note"  # or "mail.mt_comment" for a comment-type message
            )

    def action_send_certification_mail(self):
        # Load the email template
        template = self.env.ref('volunteer_management.volunteer_completion_certificate_email_template')

        if template:
            # Send the email using the template
            template.send_mail(self.id, force_send=True)

            # Render the HTML body from the template
            rendered_html_body = self.env['mail.render.mixin'].with_context({})._render_template(
                template.body_html, 'volunteer.volunteer', self.ids
            )[self.id]

            # Convert HTML to plain text
            h = html2text.HTML2Text()
            h.ignore_links = False  # Set to True if you do not want to keep links in the text
            plain_text_body = h.handle(rendered_html_body)

            # Post the plain text message to the Chatter
            self.message_post(
                body=plain_text_body,
                subject=template.subject,
                message_type='notification',  # or 'comment' depending on your needs
                subtype_xmlid="mail.mt_note"  # or "mail.mt_comment" for a comment-type message
            )

