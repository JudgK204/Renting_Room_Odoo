from odoo import models,fields
class DemoClass(models.Model):
   _name = 'cron.demo'
   student_name = fields.Char(string='Name of the student', required=True)
   def cron_demo_method(self):
       print("Inside the function")