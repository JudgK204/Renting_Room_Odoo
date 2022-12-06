from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import *
class RoomService(models.Model):
    _name='room.service'
    _parent_name="parent_id"
    _parent_store=True
    _check_company_auto=True
    name=fields.Selection([('Dạy học','Dạy học'),
                           ('Kiểm tra mail','Kiểm tra mail'),
                           ('Vệ sinh nhà','Vệ sinh nhà'),
                           ('Sửa chữa','Sửa chữa'),
                           ('Trông trẻ','Trông trẻ'),
                           ('Nấu ăn','Nấu ăn'),
                           ('Chăm sóc sức khỏe','Chăm sóc sức khỏe'),
                           ('Tư vấn','Tư vấn'),
                           ('Rèn luyện','Rèn luyện'),
                           ('Sự kiện','Sự kiện'),
                           ('An ninh','Anh ninh')], string='Service Name', required=True)
    infomation=fields.Text(string='Infomation', translate=True, company_dependent=True)
    service_price=fields.Monetary(string='Money', currency_field="currency_id")
    currency_id=fields.Many2one(comodel_name="res.currency")
    start_date=fields.Date('Start Date')
    end_date=fields.Date('End Date')
    # service_ids=fields.Many2many('room.detail',string='Room Detail', domain=[("status","=","2")])
    icon=fields.Html("Activity", sanitize=False, sanitize_tags=False,sanitize_attriutes=False,sanitize_style=True,
                     strip_style=True, strip_classes=True )
    
    company_id= fields.Many2one(comodel_name="res.company", default= lambda self: self.env.company, company_dependent=True, check_company=True)
    # rf= fields.Reference([("customer",'customer')], string= "a")
    parent_id= fields.Many2one(comodel_name="room.service", string = 'Group', ondelete="restrict")
    parent_path = fields.Char(index=True, readonly=True)

    
#=============================Constrains ngày bắt đầu phải trước ngày kết thúc======================== 
    @api.constrains('start_date','end_date')
    def _check_date(self):
        for r in self:
            if r.end_date < r.start_date:
                raise ValidationError('Invalid start or end date!')
#==============================Ghi đè create=======================================================     
    @api.model
    def create(self, vals):
        if not vals.get("infomation"):
            vals["infomation"]="Chưa có thông tin dịch vụ!"
        res= super(RoomService,self).create(vals)
        return res    
    