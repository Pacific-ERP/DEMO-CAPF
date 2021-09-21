# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    partner_type = fields.Selection([('customer', 'Client'), ('supplier', 'Fournisseur')], string="Type de partenaire")