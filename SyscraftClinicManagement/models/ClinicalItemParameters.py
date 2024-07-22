from odoo import api, models, fields


class ClinicalItemParameters(models.Model):
    _name = 'syscraft.clinical.parameters.tbl'
    _description = 'Clinical Item Parameters'
    _rec_name = 'name'

    name = fields.Char(string='Item Name ')
    section = fields.Many2one('syscraft.clinical.groups.sections.tbl', string='Clinical Section ')
    code = fields.Char(string="Code ")
    type = fields.Selection([('numeric', 'Numeric'), ('+/-', '+/-'), ('rating', 'Rating'), ('staff', 'Staff'),
                             ('text', 'Text'), ('time', 'Time'), ('yes', 'Yes'), ('no', 'No')],
                            string="Control Type on the User Interface")
    uom_id = fields.Many2one('syscraft.clinical.uom.tbl', string='Unit of Measurement ')
    sex = fields.Selection([('male', 'Male'), ('female', 'Female'), ('both', 'Both')], string='Applies to sex ')
    REF_NO = fields.Char()


class UnitOfMeasurement(models.Model):
    _name = 'syscraft.clinical.uom.tbl'
    _description = 'Clinical Unit of Measurement'
    _rec_name = 'name'

    name = fields.Char(string='Item Name ')
