# -*- coding: utf-8 -*-
from odoo import http

# class ControlCheques(http.Controller):
#     @http.route('/control_cheques/control_cheques/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/control_cheques/control_cheques/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('control_cheques.listing', {
#             'root': '/control_cheques/control_cheques',
#             'objects': http.request.env['control_cheques.control_cheques'].search([]),
#         })

#     @http.route('/control_cheques/control_cheques/objects/<model("control_cheques.control_cheques"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('control_cheques.object', {
#             'object': obj
#         })