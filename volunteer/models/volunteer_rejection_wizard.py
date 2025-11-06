from odoo import models, fields, api

class VolunteerRejectionWizard(models.TransientModel):
    _name = 'volunteer.rejection.wizard'
    _description = 'Volunteer Rejection Wizard'

    rejection_reason = fields.Text(string='Rejection Reason', required=True)

    def action_reject(self):
        """Perform the rejection action and call the existing method."""
        # Ensure that the context contains the active_id of the record to reject
        active_id = self.env.context.get('active_id')
        if active_id:
            volunteer = self.env['volunteer.volunteer'].browse(active_id)
            volunteer.write({
                'status': 'rejected',
                'rejection_reason': self.rejection_reason,
            })
            # Call the existing action_reject method on the volunteer
            volunteer.action_reject()
