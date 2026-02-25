{
    'name': 'Journal Visibility',
    'version': '19.0.0.1.0',
    'summary': 'Journal Visibility',
    'description': 'Journal Visibility',
    'author': 'LasheenTech',
    'website': '',
    'license': 'LGPL-3',
    'category': 'Accounting',
    'depends': ['base', 'account'],
    'data': [
        'security/security_viewx.xml',
        'views/account_journal_views.xml',
        'views/res_users_views.xml',
    ],
    'installable': True,
    'application': False,

}