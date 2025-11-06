{
    'name'      : 'Volunteer Management System',
    'author'    : 'Joe Mbatia',
    'version'   : '17.0',
    'category'  : 'NGO',
    'sequence'  :  20,
    'license'   : 'LGPL-3',
    'summary'   : 'Module for managing volunteers',
    'website'   : 'joembatiaportfolio.netlify.app',
    'depends'   : ['base', 'mail', 'web', 'project'],
    'data':     [
        'security/ir.model.access.csv',
        'data/volunteer_approval_email_templates.xml',
        'data/volunteer_completion_certificate_email_template.xml',
        'data/volunteer_reference_sequence.xml',
        'data/volunteer_rejection_email_templates.xml',
        'views/menu.xml',
        'views/volunteer.xml',
        'views/volunteer_rejection_wizard.xml',

    ],
    'installable': True,
    'application': True,
    'auto-install': False
}
