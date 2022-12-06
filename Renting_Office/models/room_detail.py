from odoo import fields,models,api
from odoo.exceptions import ValidationError
from datetime import *
from dateutil import relativedelta
class RoomDetail(models.Model):
    _name= 'room.detail'
    _description= 'Room Detail'
    _order='state'

    name=fields.Char(string="Room Name")
    room_address=fields.Text(string='Room Address', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today)
    size=fields.Float(string='Size', digits="OneDecimal", group_operator='sum')
    rate = fields.Integer(string='Rate')
    currency_id = fields.Many2one('res.currency', string='Currency')
    price = fields.Monetary('Price',currency_field='currency_id', group_operator='max', copy=False)
    state=fields.Selection(selection=[('1','Mới'),
                                       ('2','Đang cho thuê'),
                                       ('3','Chưa hoàn thành')],
                                       default='1',
                                       string="room status",
                                       help="Please select room status!")
    active = fields.Boolean( string='Active', default=True)
    image=fields.Image(max_width=250,max_height=370, verify_resolution=True)
        
    manager_id=fields.Many2one(comodel_name='room.manager', string='Manager', ondelete='set null')
    manager_level=fields.Selection(related="manager_id.level" ,string="Manager level")
    customer_id=fields.Many2one(comodel_name="customer", string="Customer",domain=[('state','=','renting')], states={'1':[('readonly',True),('required',False)],
                                                                                    '2':[('readonly',False),('required',True)],
                                                                                    '3':[('readonly',True),('required',False)]}, compute='_customer_state', store=True, readonly=False)
    
    
    def btn_test2(self):
        print(self)
        #print(self.search([]).mapped("contact_ids"))

#----------------------------------Chuyển đổi state-------------------------------------
    @api.depends('state')
    def _customer_state(self):
        for r in self:
            if r.state:
                if r.state!="2":
                    r.write({'customer_id': False})
            else:
                pass
                
#===============================Upper name==================================================
    @api.model
    def create(self, values):
        if values.get('name'):
            values["name"] = values["name"].upper()
        return super(RoomDetail, self).create(values)
    
    def write(self, values):
        if values.get('name'):
            values["name"] = values["name"].upper()
        return super(RoomDetail, self).write(values)
    
    @api.onchange("name")
    def _name_upper(self):
        if self.name:
            self.name= self.name.upper()
            
#--------------------------address title-------------------------------------------
    @api.model
    def create(self, values):
        print(values)
        print(self)
        if values.get('room_address'):
            values["room_address"] = values["room_address"].title()
        return super(RoomDetail, self).create(values)   
    
    def write(self, values):
        if values.get('room_address'):
            values["room_address"] = values["room_address"].title()
        return super(RoomDetail, self).write(values)
#------------------------name_get hiển thị trong model contact----------------------- 
    def name_get(self): 
        res=[]
        for r in self:
            str= r.room_address + ": "+r.name
            res.append((r.id, str))
        return res
#------------------tạo nhanh 1 record manager---------------------
    @api.model
    def name_create(self,nm):
        nc=self.create({"name":nm})
        return nc.name_get()
#----------------------------ghi đè unlink-----------------------------------------
    def unlink(self):
        return super(RoomDetail, self).unlink()
            
            
    
#===============================================================================
#=======================Test===================================================
    #-------------------read_group---------------------------------
    def button_read_group(self):
        readgroup = self.read_group(
            [("state","=","2")],   
            fields=['name',"state"],
            groupby=['currency_id','price'], lazy=False)            
        print(readgroup)
    
    def action_success(self):

        return {
            'effect':{
                'fadeout':'slow',
                'message':'Successfully',
                'type':'rainbow_man'
                }
            }    
#-------------------read----------------------------------------

    def button_read(self):
        r = self.env['room.detail'].read()           
        print(r) 
             
#-----------------browse---------------------------------------
    def button_browse(self):
        print (self.env['room.detail'].browse([1,2,8]).mapped('name'))

#-----------------search-----------------------------------------
    def button_search(self):
        #print(self.env['room.detail'].search(args=[], limit=100, order='name desc, id'))
        #print(self.env['room.detail'].search([]).mapped(lambda r : r.name=="Vina"))
        print(self.env['room.detail'].search([("name","=","Vina")]))
#-----------------name_search------------------------------------
    def button_name_search(self):
        print(self.env['room.detail'].search([]).name_search('%ina%',[('state','=','2')], operator='=like', limit=10))

#-------------------fields_get---------------------------------------
    def button_fields_get(self):
        print(self.env['room.detail'].fields_get(['name', 'size'],['type','readonly']))
    #def button_fields_view_get(self):
#--------------------filtered----------------------------------------
    def btn_filtered(self):
        #vals=self.env['room.detail'].search([]).filtered(lambda r: r.name=="BEL AIR")
        vals=self.env['room.detail'].search([]).filtered('manager_id.age').ids
        print(vals)
#--------------------filtered_domain----------------------------------------
    def btn_filtered_domain(self):
        vals=self.env['room.detail'].search([]).filtered_domain([('name','ilike','%in%')]).mapped('manager_id.name')
        print(vals)

#---------------------mapped------------------------------------------------
    def btn_mapped(self):
        vals=self.env['room.detail'].search([]).mapped('manager_id.age')
        #vals=self.env['room.detail'].search([]).mapped(lambda r: r.name=="BEL AIR")   
        # vals=self.env['room.detail'].search([]).mapped(lambda r: '%s, %s' %(r.manager_id.name,r.name))
        print(vals)
#---------------------sorted-----------------------------------------------
    def btn_sorted(self):
        vals=self.env['room.detail'].search([]).sorted(key=lambda r : r.name or r.room_address)
        print(vals)

#----------------------default_get------------------------------------------
    def btn_default_get(self):
        vals=self.env['room.detail'].search([]).default_get(['name','state','date','size','manager_id','manager_level'])
        print(vals)
        
# #----------------------name_create------------------------------------------
    def btn_name_create(self):
        r1=self.env['room.detail'].search([], limit =1)
        r2= self.env['room.detail'].search([], limit=2)
        print(r1)
        print(r2)
        print(r1 in r2)
        print(r1 <= r2)
        print(r1>=r2)
        print(r1 | r2)
        print(r1 & r2)
        print(r1 - r2)
        print(r1+r2)
#------------------------get_metadata---------------------------------------------
    def btn_get_metadata(self):
        vals=self.env['room.detail'].search([]).browse([1,2])
        print(vals.get_metadata())
        print("=================")
        print(vals.read())
#------------------------with_context--------------------------------------
    def search_all(self):
        #a=self.with_context(active_test=False).search([])
        print(self.env.context) #with_context()
        print(self.env.cr)      #
        print(self.env.uid)
        print(self.env.user)
        print(self.env)
        print(super(RoomDetail,self))
#-----------------------------ids------------------------------------------
    def btn_ids(self):
        a=self.search([]).filtered("contact_ids")
        print(a.ids)
        # print(self.env["room.detail"].with_context(active_test=False).search([]))
        # print(self.env['room.detail'].search(['|', ('active', '=', False), ('active', '=', True)]))
        print(self.name)
#----------------------------copy------------------------------------------
    def btn_copy(self):
        a=self.env["room.detail"].search([("name","like","BEL")])
        b=a.copy()
        print(b)

#----------------------------test------------------------------------------
    def btn_datetime(self):
#---------------------------subtract--------------------------------------        
        # print(fields.Date.add(fields.Date.today(),months=1))
        # print(fields.Datetime.subtract(fields.Datetime.now(), years=5))
#---------------------------to_string-------------------------------------
        # d= fields.Date.today()
        # dt=fields.Datetime.today()
        # print(type(fields.Date.to_string(d)))   #str
        # print(type(fields.Date.to_string(dt))) #str
        # print(fields.Date.to_string(dt)) #2022-11-17
        # print(fields.Datetime.to_string(d)) #2022-11-17 00:00:00
#---------------------------end_of & start_of------------------------------
        # today= fields.Date.today().replace(day=10)
        # print(fields.Date.end_of(today,'week'))
        # print(fields.Date.start_of(today,'week'))
        # now= fields.Datetime.now().replace(day=10)
        # print(fields.Datetime.start_of(now,'week'))
        # print(fields.Datetime.end_of(now,'week'))
#------------------------context_timestamp()---------------------------------
        b=self.search([("name","=","LUXURY")])
        dt_ct=fields.Datetime.context_timestamp(b, fields.Datetime.now())
        a= fields.Datetime.now()
        print(a)
        print(dt_ct)
        # # America/Yakutat
        # # 2022-11-17 04:53:34
        # # 2022-11-16 19:53:34-09:00
#------------------------context_today()-----------------------------------
        # rc=self.search([("id","=",1)])
        # c=fields.Datetime.now().replace(day=10)
        # print(c)
        # print(fields.Datetime.now())                        
        # ct= fields.Date.context_today(rc, c)
        # print(ct)
        # # 2022-11-10 04:21:11
        # # 2022-11-17 04:21:11
        # # 2022-11-09
    
    def btn_flush(self):
        a=self.env['room.detail'].search([("id","=",1)])
        print(a) 
        a.write({'name':"DD"})
        #DD vẫn chưa được nạp vào db vì chưa kết thúc hàm write (return hàm)
        # cùng lúc này nếu dùng 1 lệnh sql gọi đến name của id=1 thì name sẽ trả về data cũ
        # ngược lại nếu thêm a.flush sau khi a.write({'name':"DD"}) thì khi dùng query sẽ gọi ra name=DD
        self._cr.execute("SELECT name FROM room_detail WHERE id=1")
        print(self._cr.fetchall())

        return a # vì trong write có hàm flush nên khi kết thúc hàm write, data sẽ được đẩy vào db
    @api.model
    def btn_test_context(self, vals):
        print("context:",self.env.context)
        print("user:",self.env.user)
        print("env:",self.env)
        print("cr:",self.env.cr)
        print("su:",self.env.su)
        print("company:",self.env.company)
        print("company id:",self.env.company.id)
        
        vals= {"name":"AE", "room_address":"Hải Phòng"}
        #print(self.env["room.detail"].sudo(flag=False).search([]))
        #return super(RoomDetail, self).sudo(flag=False).create(vals)



    