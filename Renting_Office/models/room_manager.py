from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
class RoomManager(models.Model):
    _name='room.manager'
    _description='Room Manager'
    _order='manager_id'
    _parent_name="parent_id"
    _parent_store=True
    name=fields.Char('Manager Name')
    manager_id=fields.Char("Manager ID", groups="Renting_Office.room_management_group_admin")
    level=fields.Selection([('1','Môi giới'),
                          ('2','Nhân viên'),
                          ('3', 'Quản lý'),
                          ('4','Giám đốc')], 
                        default="1",                       
                        string='Level',
                        help='Please select level!',
                        required=True)
    age=fields.Integer('Age')
    phone=fields.Char('Phone Number')
    area=fields.Selection([('1','Hải Phòng'),
                          ('2','Hà Nội'),
                          ('3', 'Đà Nẵng'),
                          ('4','Tp.Hcm')],                        
                        string='Management Area',
                        help='Please select area!'
                        )
    gender=fields.Selection([('1','Nam'),
                             ('2','Nữ'),
                             ('3','Khác')], string="Gender", help="gender")
    priority=fields.Selection([
        ('0','extremely low'),
        ('1','low'),
        ('2','normal'),
        ('3','medium'),
        ('4','high'),
        ('5','very high')], string='Star rating')
    detail_ids=fields.One2many(comodel_name='room.detail',inverse_name='manager_id',limit=5,auto_join=False,string='Room Detail')
    img=fields.Image(max_width=30, max_height=30, verify_solution=True)

    parent_id=fields.Many2one(comodel_name="room.manager", string="Parent")
    parent_path= fields.Char(index=True, readonly=True)

    _sql_constraints=[("check_unique",'UNIQUE(manager_id)',"ID already exists")]
#=====================Định dạng title cho  name================================================    
    @api.onchange("name")
    def _name_title(self):
        if self.name:
            self.name= str(self.name).title()
#==================ràng buộc constraint không trùng lặp id==================
    @api.constrains("manager_id")
    def constrains_check_manager_id(self):
        for r in self:
            existing_record = self.env['room.manager'].search_count([('manager_id', '=', r.manager_id)])
            if existing_record > 1:
                raise ValidationError(('The id %s already exists!') % (r.manager_id))
           
#-------------------write 0--------------------------------------
    def button_write_0(self):
        vals=self.search([("name","like","Đinh")])
        vals.write({'detail_ids': [(0, 0, {"name":"ABC", "room_address":"hp"})]})
        print(vals.read())
        print(vals.detail_ids)
        return vals 
#-------------------write 1--------------------------------------
    def button_write_1(self):
        vals=self.search([("name","like","Đinh")])
        vals.write({'detail_ids': [(1, 44, {"name":"ABCDEF", "room_address":"DN"})]})
        print(vals.read())
        print(vals.detail_ids)
        return vals 
#-------------------write 2--------------------------------------
    def button_write_2(self):
        vals=self.search([("name","like","Đinh")])
        vals.write({'detail_ids': [(2, 44, 0)]})
        print(vals.read())
        print(vals.detail_ids)
        return vals 
#-------------------write 3--------------------------------------
    def button_write_3(self):
        vals=self.search([("name","like","Đinh")])
        vals.write({'detail_ids': [(3, 44, 0)]})
        print(vals.read())
        print(vals.detail_ids)
        return vals 
#-------------------write 4--------------------------------------
    def button_write_4(self):
        vals=self.search([("name","like","Đinh")])
        vals.write({'detail_ids': [(4, 44, 0)]})
        print(vals.read())
        print(vals.detail_ids)
        return vals 
#-------------------write 5--------------------------------------
    def button_write_5(self):
        vals=self.search([("name","like","Đinh")])
        vals.write({'detail_ids': [(5, 0, 0)]})
        print(vals.read())
        print(vals.detail_ids)
        return vals 
#-------------------write 6--------------------------------------
    def button_write_6(self):
        vals=self.search([("name","like","Đinh")])
        vals.write({'detail_ids': [(6, 0,44)]})
        print(vals.read())
        print(vals.detail_ids)
        return vals 

    def btn_fl(self):
        print(self)
        rc= self.search([("id","=",1)]).mapped("age") # lấy data từ db nạp vào cache hiện tại (age=12)
        self._cr.execute("UPDATE room_manager SET age=20 WHERE id=1")
        #update lại data với age=20 (khi đó data mới này vẫn chưa được lưu vào db mà lưu vào 1 cache riêng)
        self.invalidate_cache()
        # dùng invalidate xóa data cũ trong cache hiện tại
        print(self.search([("id","=",1)]).mapped("age")) # 20
        # trong search có flush, dùng search để đẩy data mới vào db đồng thời nạp data mới vào 
        # cache hiện tại đang trống và gọi ra (age=20)
        return rc
        
    
    

    