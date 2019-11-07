# -*- coding: utf-8 -*-
{
    'name': "Presupuestos UNAM",

    'summary': """
        Modulo de presupuestos para UNAM""",

    'description': """
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','account_accountant','project','stock','account_budget','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/seq.xml',
        'views/views.xml',
        'views/structure_view.xml',
        'views/menu_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'application':True,
    'installable':True,
}