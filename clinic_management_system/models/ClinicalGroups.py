from odoo import api, models, fields


class ClinicalGroups(models.Model):
    _name = 'syscraft.clinical.groups.tbl'
    _description = 'Clinical Groups'
    _rec_name = 'name'

    name = fields.Char(string='Clinical group Name ')
    section = fields.Many2one('syscraft.clinical.groups.sections.tbl', string='Clinical Section ')
    type = fields.Selection([('numeric', 'Numeric'), ('+/-', '+/-'), ('rating', 'Rating'), ('staff', 'Staff'),
                             ('text', 'Text'), ('time', 'Time'), ('yes', 'Yes'), ('no', 'No')], string='Type ')
    sex = fields.Selection([('male', 'Male'), ('female', 'Female'), ('both', 'Both')], string='Applies to sex ')
    item_parameter_ids = fields.One2many('syscraft.clinical.item.parameters.tbl', 'clinical_group_id')
    REF_NO = fields.Char()


class ClinicalSection(models.Model):
    _name = 'syscraft.clinical.groups.sections.tbl'
    _description = 'Clinical Sections'
    _rec_name = 'name'

    name = fields.Char(string='Clinical Section Name ')


class ItemParameters(models.Model):
    _name = 'syscraft.clinical.item.parameters.tbl'
    _description = 'Item Parameters'
    _rec_name = 'item_name_id'

    item_name_id = fields.Many2one('syscraft.product.tbl')
    item_type = fields.Char()
    clinical_group_id = fields.Many2one('syscraft.clinical.groups.tbl')
