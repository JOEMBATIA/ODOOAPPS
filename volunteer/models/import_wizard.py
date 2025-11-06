from odoo import models, fields, api
import base64
import csv
from io import StringIO


class ImportWizard(models.TransientModel):
    _name = 'volunteer.import.wizard'
    _description = 'Import Volunteer Data'

    file = fields.Binary('File', required=True)
    file_name = fields.Char('File Name')

    @api.model
    def import_file(self):
        if self.file:
            file_data = base64.b64decode(self.file)
            file_stream = StringIO(file_data.decode('utf-8'))
            reader = csv.DictReader(file_stream)

            for row in reader:
                self.env['my.model'].create({
                    'name': row['name'],
                    'email': row['email'],
                    'status': row['status'],
                    'phone': row['phone'],
                    'address': row['address'],
                    'gender': row['gender'],
                    'country_id': self.env['res.country'].search([('name', '=', row['country_id'])], limit=1).id,
                    'mode': row['mode'],
                    'identification': row['identification'],
                    'message': row['message'],
                    'hobbies': row['hobbies'],
                    'emergency_phone': row['emergency_phone'],
                    'emergency_details': row['emergency_details'],
                    'area_of_interest': row['area_of_interest'],
                    'date_of_birth': row['date_of_birth'],
                    'start_date': row['start_date'],
                    'end_date': row['end_date'],
                })
        return {'type': 'ir.actions.act_window_close'}
