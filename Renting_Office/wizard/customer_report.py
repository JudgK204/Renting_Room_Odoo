from odoo import models,api,fields

class CustomerReport(models.TransientModel):
    _name='customer.report'
    
    address= fields.Text(string='Customer')
    def action_confirm(self):
        customer_id=self.env["customer"].browse(self.env.context['active_ids'])
        new_data={}
        if self.address:
            new_data.update({'address': self.address})
            customer_id.write(new_data)
        
           