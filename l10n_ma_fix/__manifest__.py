# -*- coding: utf-8 -*-
{
    'name': "l10n_ma_fix",

    'description': """
        Mise a jour et correction de la localisation MAROC ODOO du meetup du 15 juin 2019 
    """,

    'author': "BADEP, HORIYASOFT, PRAGMATIC SYSTEM",
    'website': "https://badep.ma, http://www.horiyasoft.ma, http://www.pragmatic-system.ma",

    'category': 'Technical',
    'version': '0.1',

    'depends': ['l10n_ma'],
    'auto_install': False,

    'data': [
        'data/account_tax_data.xml',
        'data/l10n_ma_chart_data.xml',
        'data/res_country_data.xml',
        'views/report_invoice.xml',
    ],
}
