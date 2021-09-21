# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def _compute_journal_domain_and_types(self):
        res = super(AccountPayment, self)._compute_journal_domain_and_types()

        if self.payment_type == 'outbound':
            # control if setting is enable.
            # allow only cash type, not bank
            journal_type = ['cash']
            res["journal_types"] = set(journal_type)

            # only show journal_id matching partner_type
            domain = res["domain"]
            domain.append(('partner_type', '=', 'supplier'))

        elif self.payment_type == 'inbound':
            # control if setting is enable.
            # allow only cash type, not bank
            journal_type = ['cash']
            res["journal_types"] = set(journal_type)

            # only show journal_id matching partner_type
            domain = res["domain"]
            domain.append(('partner_type', '=', 'customer'))

        return res