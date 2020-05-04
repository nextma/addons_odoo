# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountAccount(models.Model):
    _inherit = 'account.account'

    @api.model
    #Mise à jour des sociétés existantes. Les nouvelles sociétés auront le paramétrge automatique
    def init_migration(self):
        for company in self.env['res.company'].search([('chart_template_id', '=', self.env.ref('l10n_ma.l10n_kzc_temp_chart').id)]):
            self.env['ir.property'].search([('name', '=', 'property_account_receivable_id'), ('company_id', '=', company.id)]).write({
                'value_reference': 'account.account,' + str(self.env.ref('l10n_ma.' + str(company.id) +'_pcg_34211').id)})
            self.env['ir.property'].search([('name', '=', 'property_account_payable_id'), ('company_id', '=', company.id)]).write({
                'value_reference': 'account.account,' + str(self.env.ref('l10n_ma.' + str(company.id) +'_pcg_4411').id)})
            self.env['ir.property'].search([('name', '=', 'property_account_expense_categ_id'), ('company_id', '=', company.id)]).write({
                'value_reference': 'account.account,' + str(self.env.ref('l10n_ma.' + str(company.id) +'_pcg_6111').id)})
            company.write({
                'account_sale_tax_id': self.env.ref('l10n_ma.' + str(company.id) +'_tva_vt20').id,
                'account_purchase_tax_id': self.env.ref('l10n_ma.' + str(company.id) +'_tva_ac20').id,
                'tax_exigibility': True,
            })
            #Créer position fiscale étranger
            #TODO: Ne pas créer de position fiscale à la mise à jour du module ou si la position fiscale "étranger" est déjà dans le système
            self.env['account.fiscal.position'].create({
                'name': 'Etranger',
                'company_id': company.id,
                'tax_ids': [(0, 0, {'tax_src_id': self.env.ref('l10n_ma.' + str(company.id) +'_tva_vt20').id, 'tax_dest_id': self.env.ref('l10n_ma.' + str(company.id) +'_tva_exo').id}), (0, 0, {'tax_src_id': self.env.ref('l10n_ma.' + str(company.id) +'_tva_ac20').id, 'tax_dest_id': self.env.ref('l10n_ma.' + str(company.id) +'_tva_exo').id})],
                'account_ids': [(0, 0, {'account_src_id': self.env.ref('l10n_ma.' + str(company.id) +'_pcg_7111').id, 'account_dest_id': self.env.ref('l10n_ma.' + str(company.id) +'_pcg_7113').id})]
            })
            self.env['account.journal'].create({
                'name': 'Chèques',
                'type': 'bank',
                'code': 'CHQ',
                'company_id': company.id,
                'default_debit_account_id': self.env.ref('l10n_ma.' + str(company.id) +'_pcg_51111').id,
                'default_credit_account_id': self.env.ref('l10n_ma.' + str(company.id) +'_pcg_51111').id,
                'post_at_bank_rec': True
            })
            self.env['account.tax'].search([('company_id', '=', company.id), ('type_tax_use', '=', 'sale')]).write({
                'tax_exigibility': 'on_payment',
                'cash_basis_account_id': self.env.ref('l10n_ma.' + str(company.id) +'_pcg_4456').id,
                'cash_basis_base_account_id': self.env.ref('l10n_ma.' + str(company.id) +'_pcg_7111').id
            })
            self.env['account.tax'].search([('company_id', '=', company.id), ('type_tax_use', '=', 'purchase')]).write({
                'tax_exigibility': 'on_payment',
                'cash_basis_account_id': self.env.ref('l10n_ma.' + str(company.id) +'_pcg_3456').id,
                'cash_basis_base_account_id': self.env.ref('l10n_ma.' + str(company.id) +'_pcg_6111').id
            })