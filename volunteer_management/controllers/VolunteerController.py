from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)


class VolunteerController(http.Controller):

    @http.route('/get_states/<int:country_id>', type='json', auth='public')
    def get_states(self, country_id):
        states = request.env['res.country.state'].search([('country_id', '=', country_id)])
        state_data = [{'id': state.id, 'name': state.name} for state in states]
        return {'states': state_data}

    @http.route('/volunteer-form', type='http', auth='user', website=True)
    def volunteer_form(self, **kwargs):
        values = {
            'volunteer_name': request.env.user.name,
            'volunteer_email': request.env.user.email,
        }
        return request.render('volunteer_management.create-volunteer', values)

    @http.route('/volunteer/register', type='http', auth='user', methods=['POST'], website=True)
    def register(self, **kwargs):
        _logger.info('Received kwargs: %s', kwargs)
        # Extract form data
        identification = kwargs.get('identification')
        name = kwargs.get('name')
        email = kwargs.get('email')
        phone = kwargs.get('phone')
        gender = kwargs.get('gender')
        address = kwargs.get('address')
        country_id = int(kwargs.get('country_id'))
        project_ids = [(6, 0, [int(kwargs.get('project_ids'))])]
        mode = kwargs.get('mode')
        message = kwargs.get('message')
        hobbies = kwargs.get('hobbies')
        emergency_phone = kwargs.get('emergency_phone')
        emergency_name = kwargs.get('emergency_name')
        emergency_relationship = kwargs.get('emergency_relationship')
        emergency_details = kwargs.get('emergency_details')
        date_of_birth = kwargs.get('date_of_birth')
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        area_of_interest = kwargs.get('area_of_interest')


        if not project_ids:
            return "Program ID is required"

        if country_id is not None:
            country_id = int(country_id)
        else:
            _logger.warning('country_id is None')

        try:
            # Save the data in the custom model
            request.env['volunteer.volunteer'].sudo().create({
                'identification': identification,
                'name': name,
                'email': email,
                'phone': phone,
                'gender': gender,
                'address': address,
                'country_id': country_id,
                'project_ids': project_ids,
                'mode': mode,
                'message': message,
                'hobbies': hobbies,
                'emergency_name': emergency_name,
                'emergency_phone': emergency_phone,
                'emergency_relationship': emergency_relationship,
                'emergency_details': emergency_details,
                'date_of_birth': date_of_birth,
                'end_date': end_date,
                'start_date': start_date,
                'area_of_interest': area_of_interest,
                'status': 'pending',
            })

        except Exception as e:
            print(f"Error creating volunteer: {e}")
            return f"Error creating volunteer: {e}"

            # Redirect to a thank you page or show a success message

        return request.redirect('/volunteer-thank-you')

        # @http.route('/thank-you', type='http', auth='user', website=True, csrf=False)
        # def thank_you(self, **kwargs):
        #     return request.render('volunteer_dynamic_snippet.thank_you_page', {})
