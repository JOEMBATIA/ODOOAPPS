from odoo import models, fields, api

class Project (models.Model):
    _inherit = 'project.project'

    country_id = fields.Many2one('res.country')
    state_id = fields.Many2one('res.country.state', domain="[('country_id', '=?', country_id)]", string='City/County',
                               tracking=True)
    image = fields.Image()
