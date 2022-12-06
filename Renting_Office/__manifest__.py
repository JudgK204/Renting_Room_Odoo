{
 'name': "Renting Office",
'summary': "Room management",
'description': """
What it does
============
The module provides management education features.
Key Features
============
""",
'author': "Your name",
'sequence':-1000,
'application':True,
'installable':True,
'demo':[],
'website': "https://viindoo.com",
'category': 'Uncategorized',
'version': '0.1.0',
'depends': ['base','account'],
'auto_install':True,
# 'demo': ['demo.xml'], 
'data': [
'security/security.xml',
'security/ir.model.access.csv',
'data/room_detail.xml',
'data/room_manager.xml',
'data/customer_sequence.xml',
'views/room_management_views.xml',
'views/room_detail_views.xml',
'views/room_manager_views.xml',
'views/customer_views.xml',
'views/room_service_views.xml',
'wizard/customer_report_views.xml',
'views/contact_view.xml'
   ],
}
