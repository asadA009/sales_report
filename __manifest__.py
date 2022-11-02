# -*- coding: utf-8 -*-
{
    'name': 'Sales Report',
    'version': '1.0',
    'category': 'base',
    'summary': '',
    'description': """""",
    'author': 'Asad Ali',
    'website': '',
    'depends': ['sale', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/account_move_dynamic.xml',
        'views/account_payment_inherit.xml',
        'report/sales_report_views.xml',
        'report/sales_report_excel.xml',
        'wizard/sales_report_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
}
