{
    'name': 'Volunteer Snippet',
    'version': '17.0.0.1',
    'description': 'Volunteer Snippet',
    'summary': 'Volunteer Snippet',
    'author': 'Joe',
    'category': 'website',
    'depends': ['website'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/volunteer_snippet.xml',
        'views/thank_you_page.xml',
        'views/volunteer_registration_views.xml',
    ],
    # 'assets': {
    #     'web.asssests_frontend': [
    #         'volunteer_snippet/static/src/js/volunteer_snippet.js',
    #         'volunteer_snippet/static/src/css/volunteer_snippet.css'
    #     ],
    #     'web.assets_qweb': [
    #         'volunteer_snippet/static/src/xml/volunteer_snippet.xml'
    #     ]
    # }

    'installable': True,
    'application': True,
}
