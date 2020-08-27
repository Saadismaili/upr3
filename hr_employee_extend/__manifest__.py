# -*- encoding: utf-8 -*-

{
    'name': 'Custom Employees',
    'version': '1.0',
    'author': 'Andema',
    'website': 'http://www.andemaconsulting.com',
    "depends": [
        'hr'
    ],
    'data': [
        "views/hr_employee_views.xml",
        # "report/daily_activity_report.xml",
        ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
