# -*- coding: utf-8 -*-
from odoo import http

# class Presupuestos(http.Controller):
#     @http.route('/presupuestos/presupuestos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/presupuestos/presupuestos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('presupuestos.listing', {
#             'root': '/presupuestos/presupuestos',
#             'objects': http.request.env['presupuestos.presupuestos'].search([]),
#         })

#     @http.route('/presupuestos/presupuestos/objects/<model("presupuestos.presupuestos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('presupuestos.object', {
#             'object': obj
#         })