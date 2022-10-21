# -*- coding: utf-8 -*-
{
    'name': 'Sales Report',
    'version': '1.0',
    'category': 'base',
    'summary': '',
    'description': """""",
    'author': 'Asad Ali',
    'website': '',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/account_move_dynamic.xml',
        'report/sale_report_views.xml',
        'wizard/sales_report_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
}