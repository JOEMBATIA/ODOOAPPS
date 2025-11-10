from odoo import api, models, fields


class InvestigationTools(models.Model):
    _name = 'syscraft.investigation.tool.tbl'
    _description = 'Investigations Tool'

    name = fields.Char(string="Investigation Name ")
    investigation_code = fields.Char(string="Code ")
    type = fields.Selection([('lab', 'Lab'), ('radiology', 'Radioology')])
    category_id = fields.Many2one('syscraft.investigation.category.tbl', string='Category ')
    service = fields.Many2one('syscraft.expense.service.category.tbl', string='Service')
    #lab = fields.Many2one('')
    cost_price = fields.Integer(string='Cost Price (KSH) ')
    price = fields.Integer(string='Price (KSH)')
    instructions = fields.Text(string="Patient Instructions")
    clinical_group = fields.Many2one('syscraft.clinical.groups.tbl')
    result_text = fields.Char(string="Result Text ")
    sex = fields.Selection([('male', 'Male'), ('female', 'Female'), ('both', 'Both')], string='Applies to sex ')
    item_parameter_line_ids = fields.One2many('syscraft.investigation.item.parameters.tbl', 'tools_investigation_id')
    REF_NO = fields.Char()
    attachment = fields.Binary(string='Patient Handouts', attachment=True)
    attachment_filename = fields.Char(string='Patient Handout Filename')
    specimen = fields.Many2one('syscraft.category.specimen.tbl', string="Specimen ")
    specimen_storage = fields.Many2one('syscraft.category.specimen.tbl', string="Specimen Storage")
    method = fields.Many2one('syscraft.category.storage.tbl', string="Method ")


class Category(models.Model):
    _name = 'syscraft.investigation.category.tbl'
    _description = 'Category Details'

    item = fields.Char(string='Item')
    value = fields.Char(string='Value')


class Specimen(models.Model):
    _name = 'syscraft.category.specimen.tbl'
    _description = 'Specimen Details'

    specimen_name = fields.Char(string='Specimen Name')


class SpecimenStorage(models.Model):
    _name = 'syscraft.category.storage.tbl'
    _description = 'Specimen Storage Details'

    specimen_storage_name = fields.Char(string='Specimen Storage Name ')


class Method(models.Model):
    _name = 'syscraft.category.method.tbl'
    _description = 'Method Details'

    method_name = fields.Char(string='Method Name ')


class ItemParameters(models.Model):
    _name = 'syscraft.investigation.item.parameters.tbl'
    _description = 'Investgiation Item parameters'

    name = fields.Char()
    unit = fields.Char()
    type = fields.Char()
    range = fields.Char(string="REF.RANGE")
    tools_investigation_id = fields.Many2one('syscraft.investigation.item.parameters.tbl')
