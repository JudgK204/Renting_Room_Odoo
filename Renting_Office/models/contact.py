from odoo import models, fields
class Contact(models.Model):
    _inherit="customer"
    
    #room_id=fields.Char(string="AC")
    service_ids= fields.Many2many(comodel_name="room.service", string="Room Service")
    

#----------------------cr.execute----------------
        # self.flush()
        # query="SELECT * FROM customer"
        # self.env.cr.execute(query)
        # a=self.env.cr.dictfetchall()
        # print(a)


    