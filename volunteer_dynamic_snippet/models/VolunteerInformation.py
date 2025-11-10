from odoo import fields, api, models


class Volunteer(models.Model):
    _name = 'volunteer.volunteer'
    _description = 'Volunteer information'

    lang = fields.Char(string="Language")
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    status = fields.Selection(
        [('rejected', 'Rejected'), ('to be approved', 'To be Approved'), ('approved', 'Approved')],
        string="Application Status", default="pending")
    project_ids = fields.Many2many('project.project', string='Projects')
    image = fields.Image(string="Image", tracking=True)
    phone = fields.Char(string='Phone')
    address = fields.Char(string='Address')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender')
    country_id = fields.Many2one('res.country')
    state_id = fields.Many2one('res.country.state', domain="[('country_id', '=?', country_id)]", string='City/State')
    mode = fields.Selection([('onsite', 'Onsite'), ('remote', 'Remote/Online'), ('hybrid', 'Hybrid')])
    identification = fields.Char(string='Passport/National ID', required=True)
    message = fields.Text(string='Reason you are joining us')
    signup_url = fields.Char(compute='_compute_signup_url')

    def _get_signup_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/volunteer/signup/{self.id}"

    def _compute_signup_url(self):
        for record in self:
            record.signup_url = record._get_signup_url()
