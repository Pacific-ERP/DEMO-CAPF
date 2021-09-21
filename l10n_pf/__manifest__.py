# -*- coding: utf-8 -*-
{
    'name': "Polynésie Française - Accounting",

    'summary': """
This is the module to manage the accounting chart for French Polynesia in Odoo.
    """,

    'description': """
This is the module to manage the accounting chart for French Polynesia in Odoo.

This module applies to companies based in French Polynesia.
    """,

    'author': "Pacific-ERP.com",
    'category': 'Localization',
    'version': '1.0.3',
    'depends': ['account', 'base_iban', 'base_vat', 'account_batch_payment'],
    'data': [
        # security
        'security/ir.model.access.csv',
        'security/multi_currencies.xml',
        'security/security.xml',

        # data
        'data/account_chart_template.xml',
        'data/account_account_template.xml',
        'data/account_tax_group.xml',
        'data/product_category_data.xml',
        'data/res_bank.xml',

        # views
        # 'views/account_journal_dashboard_view.xml',
        'views/account_account_views.xml',
        'views/account_batch_payment_views.xml',
        'views/account_journal_views.xml',
        'views/account_move_line_views.xml',
        'views/account_move_views.xml',
        'views/account_reconcile_model_views.xml',
        'views/product_views.xml',
        ],
}
