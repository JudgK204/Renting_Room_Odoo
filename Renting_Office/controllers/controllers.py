# -*- coding: utf-8 -*-
# from odoo import http


# class QuanLyPhong(http.Controller):
#     @http.route('/quan_ly_phong/quan_ly_phong/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/quan_ly_phong/quan_ly_phong/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('quan_ly_phong.listing', {
#             'root': '/quan_ly_phong/quan_ly_phong',
#             'objects': http.request.env['quan_ly_phong.quan_ly_phong'].search([]),
#         })

#     @http.route('/quan_ly_phong/quan_ly_phong/objects/<model("quan_ly_phong.quan_ly_phong"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('quan_ly_phong.object', {
#             'object': obj
#         })
