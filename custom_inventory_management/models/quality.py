from odoo import models, fields, api


class QualityCheck(models.Model):
    _inherit = 'quality.check'

    custom_quality_notes = fields.Text(string='Quality Notes')
    inspection_date = fields.Datetime(string='Inspection Date', default=fields.Datetime.now)
    inspector_id = fields.Many2one('res.users', string='Inspector', default=lambda self: self.env.user)