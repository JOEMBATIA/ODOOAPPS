from odoo import fields, models, api


class Tools(models.Model):
    # defines the table name inside the database
    _name = "syscraft.clinic.tools.tbl"
    _inherit = "mail.thread"
    _description = "Tools records"

    # defining fields ie columns in the table
    CATEGORIES = fields.Selection([('All Categories', 'All Categories'), ('Corporate', 'Corporate'),
                                   ('External Practitioners', 'External Practitioners'), ('Vendor', 'Vendor'),
                                   ('Insurance Group', 'Insurance Group')], string="All Categories ")
    NAME = fields.Char(string="Name ")
    EMAIL = fields.Char(string="Email Address ")
    WEBSITE = fields.Char(string="Website ")
    IMAGE = fields.Image(string="")
    CONTACT_PERSON = fields.Char(string="Contact Person ")
    CP_PHONE = fields.Integer(string="Contact Person Phone(+254) ")
    MOBILE = fields.Integer(string="Mobile No. ", required=True)
    PHONE1 = fields.Integer(string="Phone No1(+254). ")
    PHONE2 = fields.Integer(string="Phone No2(+254). ")
    SKYPE = fields.Integer(string="Skype ID ")
    FAX = fields.Integer(string="Fax(+254) ")
    FINANCIAL_SUMMARY = fields.Text(string="Financial Summary ")
    ADDRESS1 = fields.Char(String="Address1 ", required=True, tracking=True)
    ADDRESS2 = fields.Char(String="Address2 ", tracking=True)
    ADDRESS3 = fields.Char(String="Address3 ", tracking=True)
    CITY = fields.Char(String="Address3 ", tracking=True)
    POST_CODE = fields.Char(String="Address3 ", tracking=True)
    STATE = fields.Char(String="State ", tracking=True)
    COMPANY_ID = fields.Char(String="State ", tracking=True)
    COUNTRY = fields.Selection([('NIGERIA', 'NIGERIA'), ('KENYA', 'KENYA'), ('ALGERIA', 'ALGERIA'),
                                ('ALGERIA', 'ALGERIA'), ('AFGHANISTAN', 'AFGHANISTAN'), ('ANDORRA', 'ANDORRA'),
                                ('BULGARIA', 'BULGARIA'), ('BOTSWANA', 'BOTSWANA')], String="Country ")

