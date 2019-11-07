# -*- coding: utf-8 -*-
{
    'name': "Control de cheques UNAM",

    'summary': """
        Modulo para asignacion y control de cheques de la UNAM""",

    'description': """
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'installable' : True,
    'aplication' : True,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}