from odoo import api, models, fields


class ImmunizationSchedule(models.Model):
    _name = 'syscraft.immunization.schedule.tbl'
    _description = 'Immunization Schedule'
    _rec_name = 'name'

    name = fields.Char(string='Immunization Name ')
    schedule_start = fields.Selection([('Date of Assignment', 'Date of Assignment'),
                                       ('Date of Birth', 'Date of Birth')], string='Schedule Starts From ')
    immunisation_item_ids = fields.One2many('syscraft.immunization.item.tbl', 'immunization_schedule_id')
    REF_NO = fields.Char()


class ImmunizationItems(models.Model):
    _name = 'syscraft.immunization.item.tbl'
    _description = 'Immunization Items'
    _rec_name = 'immunisation_item_id'

    immunisation_item_id = fields.Many2one('syscraft.immunization.item.lines.tbl')
    interval = fields.Char()
    immunization_schedule_id = fields.Many2one('syscraft.immunization.schedule.tbl')


class ImmunizationItemLine(models.Model):
    _name = 'syscraft.immunization.item.lines.tbl'
    _description = 'Immunization Items'
    _rec_name = 'immunisation_item'

    immunisation_item = fields.Char(string="Immunization Item Name")
    quantity = fields.Integer(string="QTY ")
    price = fields.Float(string="Price(KSH) ")
