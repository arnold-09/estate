
{
    'name': 'Estate',
    'version': '1.0',
    'author': 'Your Name',
    'category': 'Real Estate',
    'summary': 'Real Estate Management Module',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        #'views/res_users_views.xml',
        'views/estate_property_kanban_views.xml',
        'data/estate_data.xml',
         'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
}