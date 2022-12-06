from odoo import fields,models
from attr import field

class RoomManagement(models.Model):
    _name= 'room.management'
    _description= 'Room Management'
    # _inherit={'room.manager'}
    
    name=fields.Html('name')
    
    # def a_success(self):
    #     return {
    #         'effect':{
    #             'fadeout':'slow',
    #             'message':'Successfully',
    #             'type':'rainbow_man'
    #             }
    #         }  