from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)


class VolunteerController(http.Controller):

    @http.route('/volunteer/register', type='http', auth='user', methods=['POST'], website=True, csrf=False)
    def register(self, **kwargs):
        _logger.info('Received kwargs: %s', kwargs)
        # Extract form data
        identification = kwargs.get('identification')
        name = request.env.user.name
        email = request.env.user.name
        phone = kwargs.get('phone')
        gender = kwargs.get('gender')
        address = kwargs.get('address')
        country_id = int(kwargs.get('country_id'))
        state_id = int(kwargs.get('state_id'))
        project_ids = [(6, 0, [int(kwargs.get('project_ids'))])]
        mode = kwargs.get('mode')
        message = kwargs.get('message')

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
                'state_id': state_id,
                'project_ids': project_ids,
                'mode': mode,
                'message': message,
                'status': 'pending',
            })

        except Exception as e:
            print(f"Error creating volunteer: {e}")
            return f"Error creating volunteer: {e}"

            # Redirect to a thank you page or show a success message
            # return request.render('volunteer_dynamic_snippet.thank_you_page', {})

        return request.redirect('/volunteer-thank-you')

        # @http.route('/thank-you', type='http', auth='user', website=True, csrf=False)
        # def thank_you(self, **kwargs):
        #     return request.render('volunteer_dynamic_snippet.thank_you_page', {})
