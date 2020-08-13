# -*- encoding: utf-8 -*-

{
    'name': 'Activités Journalières',
    'version': '1.0',
    'author': 'Andema',
    'website': 'http://www.andemaconsulting.com',
    "depends": [
        'hr'
    ],
    'data': [
        "security/ir.model.access.csv",
        "views/daily_activity_views.xml",
        # "report/daily_activity_report.xml",
        ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
