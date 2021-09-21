# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _, tools


class ChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    def _load(self, sale_tax_rate, purchase_tax_rate, company):
        res = super(ChartTemplate,self)._load(sale_tax_rate, purchase_tax_rate, company)

        # Set suspense account
        domain = [
            ('company_id', '=', company.id),
            ('type', '=', 'cash'),
            ('suspense_account_id', '=', False),
        ]
        journals = self.env['account.journal'].search(domain)
        journals.write({'suspense_account_id' : self.env.company.account_journal_suspense_account_id.id})

        return res

    def _prepare_all_journals(self, acc_template_ref, company, journals_dict=None):
        """
        Override method to add/update data for journals
        :param acc_template_ref: Char Template
        :param company: company
        :param journals_dict: base disctionnay
        :return: A dictionnary with all values to create journals.
        """

        def _update_existing_journals(journals):
            """
            Update existing journals
            """
            for journal in journals:
                if journal['type'] in ['sale', 'purchase']:
                    journal['refund_sequence'] = True
                if journal['code'] == 'MISC':
                    journal['name'] = 'OPÉRATIONS DIVERSES'
                    journal['code'] = 'OD'
                if journal['code'] == 'EXCH':
                    journal['name'] = 'DIFFÉRENCE DE CHANGES'
                    journal['code'] = 'EXCH'
                if journal['type'] == 'sale':
                    journal['sequence'] = 1
                    journal['name'] = 'VENTES'
                    journal['code'] = 'VTE'
                    journal['default_account_id'] = self.env.ref('l10n_pf.%s_pcg_7071' % self.env.company.id).id
                if journal['type'] == 'purchase':
                    journal['sequence'] = 2
                    journal['name'] = 'ACHATS'
                    journal['code'] = 'ACH'
                    journal['default_account_id'] = self.env.ref('l10n_pf.%s_pcg_6071' % self.env.company.id).id

        def _get_default_account(journal_vals, type='debit'):
            """
            Return the default account
            :param journal_vals: values for the journal
            :param type: is debit or credit ?
            :return: The default account
            """
            default_account = False

            # CHEQUES
            if journal_vals['code'] == 'CHQF':
                return self.env.ref('l10n_pf.%s_pcg_5115' % self.env.company.id).id
            if journal_vals['code'] == 'CHQC':
                return self.env.ref('l10n_pf.%s_pcg_5112' % self.env.company.id).id
            # CASH
            if journal_vals['code'] in ('CASHC', 'CASHF'):
                return self.env.ref('l10n_pf.%s_pcg_5300' % self.env.company.id).id
            # CB
            if journal_vals['code'] == 'CB':
                return self.env.ref('l10n_pf.%s_pcg_5802' % self.env.company.id).id
            # VIS
            if journal_vals['code'] == 'VISA':
                return self.env.ref('l10n_pf.%s_pcg_5803' % self.env.company.id).id
            # AMEX
            if journal_vals['code'] == 'AMEX':
                return self.env.ref('l10n_pf.%s_pcg_5804' % self.env.company.id).id

            return default_account

        def _add_extras_journals(journals):
            """
            Add extras journals in journals
            :param journals: Disct holding all journal to create
            """
            extra_journals = [
                {'name': _('ESPECES'), 'type': 'cash', 'code': 'CASHC', 'favorite': True, 'sequence': 14, 'partner_type': 'customer'},
                {'name': _('ESPECES'), 'type': 'cash', 'code': 'CASHF', 'favorite': True, 'sequence': 15, 'partner_type': 'supplier'},
                {'name': _('CHEQUES'), 'type': 'cash', 'code': 'CHQC', 'favorite': True, 'sequence': 20, 'partner_type': 'customer'},
                {'name': _('CHEQUES'), 'type': 'cash', 'code': 'CHQF', 'favorite': True, 'sequence': 21, 'partner_type': 'supplier'},
                {'name': _('CB'), 'type': 'cash', 'code': 'CB', 'favorite': False, 'sequence': 23, 'partner_type': 'customer'},
                {'name': _('VISA'), 'type': 'cash', 'code': 'VISA', 'favorite': False, 'sequence': 24, 'partner_type': 'customer'},
                {'name': _('AMEX'), 'type': 'cash', 'code': 'AMEX', 'favorite': False, 'sequence': 25, 'partner_type': 'customer'},
            ]
            for extra_journal in extra_journals:
                vals = {
                    'type': extra_journal['type'],
                    'partner_type': extra_journal['partner_type'],
                    'name': extra_journal['name'],
                    'code': extra_journal['code'],
                    'company_id': company.id,
                    'default_account_id': _get_default_account(extra_journal, 'credit'),
                    'loss_account_id': self.env.ref('l10n_pf.%s_pcg_658' % self.env.company.id).id,
                    'profit_account_id': self.env.ref('l10n_pf.%s_pcg_758' % self.env.company.id).id,
                    'show_on_dashboard': extra_journal['favorite'],
                    'color': extra_journal.get('color', False),
                    'sequence': extra_journal['sequence'],
                }
                journals.append(vals)

        """
        MAIN
        """
        # Execute Super to get default data
        journals = super(ChartTemplate, self)._prepare_all_journals(acc_template_ref, company, journals_dict)

        # Update values of existing journals
        _update_existing_journals(journals)

        # Add extras journals
        _add_extras_journals(journals)

        self.env.company.currency_provider = 'xe_com'
        self.env.company.currency_interval_unit = 'daily'
        self.env.company.invoice_is_print = False

        return journals
