from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import *
from dateutil import relativedelta
class Customer(models.Model):
    _name="customer"
    _description="customer infomation"
    _order='state'
    _rec_name="customer_id"

    name=fields.Char('Customer Name')
    image= fields.Image(max_width=50, max_height=70, verify_resolution=True)
    customer_id= fields.Char('ID Customer', readonly=True)
    address=fields.Text('Address')
    dob=fields.Date('Date of birth')
    age=fields.Integer(compute='_compute_age',inverse="_inverse_compute_age", search="_search_age",store=False)
    phone_number=fields.Char('Phone Number')
    note=fields.Text('Note')
    avatar=fields.Binary(string="Avatar", prefetch=False,attachment=False)
    gender=fields.Selection([('1','Nam'),
                        ('2','Nữ'),
                        ('3','Khác')],
                        string='Gender',                      
                        help=("Select gender!"),
                        default='1'
                        )
    state = fields.Selection(string='Status', selection=[("new","Khách hàng mới"),
                                                         ('renting', 'Khách đang thuê'),
                                                         ('old', 'Khách hàng cũ')], default="new") 
    room_ids= fields.One2many(comodel_name="room.detail", inverse_name="customer_id", string="Room", compute="_room_state", store=True, readonly=False)
    
    company_id= fields.Many2one("res.company", default= lambda self: self.env.company, company_dependent=True)
    @api.depends('state')
    def _room_state(self):
        for r in self:
            if r.state:
                if r.state!='renting':
                    r.write({'room_ids':[(5,0,0)]})
            else:
                pass
#=================================================================================
    def create(self,vals):
        if vals.get('address'):
            vals['address']=vals['address'].title()
        return super(Customer,self).create(vals)
    
    def write(self,vals):
        if vals.get('address'):
            vals['address']=vals['address'].title()
        return super(Customer,self).write(vals)
#=================================================================================
    def name_get(self):
        res=[]
        for r in self:
            ng= r.customer_id + " - "+r.name
            res.append((r.id,ng))
        return res
            
#=====================tạo trình tuần tự sequence==========================
    @api.model
    def create(self,vals):
        vals['customer_id']=self.env['ir.sequence'].next_by_code('customer.sequence.id')
        return super(Customer,self).create(vals)
        
#====================tính toán tuổi=======================================
    @api.depends('dob')
    def _compute_age(self):
        for r in self:
            if r.dob:
                r.age = fields.Date.today().year - r.dob.year
            else:
                r.age=0
                              
    @api.onchange("dob")
    def _onchange_dob(self):
        if self.dob == False:
            self.age = 0
        else:
            self.age = fields.Date.today().year - self.dob.year
#===================== tính năm sinh=====================================        

    def _inverse_compute_age(self):
        today= date.today()
        for r in self:
            if r.age:
                r.dob= today- relativedelta.relativedelta(years=r.age)
    
#============================chuyển đổi trạng thái status của khách hàng================  
    @api.model    
    def is_allowed_state(self, current_state, new_state):
        allowed_states = [('new', 'old'), ('new', 'renting'), ('renting', 'old')]
        return (current_state, new_state) in allowed_states
    def change_customer_state(self, state):
        for c in self:
            if c.is_allowed_state(c.state, state):
                c.state = state
            else:
                raise UserError(_("Changing customer status from %s to %s is not allowed.") % (c.state, state))
    
    def change_to_new(self):
        self.change_customer_state('new')

    def change_to_renting(self):
        self.change_customer_state('renting')

    def change_to_off(self):
        self.change_customer_state('old')
        
#============================search compute=============================
    def btn_search(self):
        a=self.env["customer"].search([('age', '!=', 23)]).mapped("age")
        print(a)

    