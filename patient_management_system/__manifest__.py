{
    'name': 'Patient Management System',
    'version': '1.0',
    'sequence': 30,
    'category': 'Healthcare',
    'summary': 'Manage patient information, expenses, progress, and reports.',
    'depends': ['base', 'mail', 'account'],
    'data': [
        'views/menu.xml',
        'views/patient_view.xml',
        'views/expense_view.xml',
        'views/progress_view.xml',
        'views/dashboard_view.xml',
        'views/report_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
