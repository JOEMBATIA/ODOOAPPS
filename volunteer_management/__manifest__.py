{
    "name": "Volunteer Management System",
    "author": "Joe Mbatia",
    "version": "1.0",
    "category": "NGO",
    "sequence": 20,
    "license": "LGPL-3",
    "summary": "Module for managing volunteers",
    "website": "www.syscraft.co.ke",
    "depends": ["base", "mail", "website", "project"],
    "data": [
        "security/ir.model.access.csv",
        "data/volunteer_reference_sequence.xml",
        "data/volunteer_approval_email_templates.xml",
        "data/volunteer_completion_certificate_email_template.xml",
        "data/volunteer_rejection_email_templates.xml",
        "views/volunteer_model_actions.xml",
        "views/volunteer_rejection_wizard.xml",
        "views/project_project_view.xml",
        "views/menu.xml",
        "views/volunteer.xml",
        "views/web_form.xml",

    ],
    'assets': {
        'web.assets_frontend': [
            'volunteer_management/static/src/scss/volunteer_form.scss',
            'volunteer_management/static/src/js/volunteer_form.js',
            'volunteer_management/static/src/js/web-form-validations.js'
        ],
    },
    'qweb': [
        'static/src/xml/column_toggle.xml',
    ],

    'installable': True,
    'application': True,
    'auto-install': False
}
