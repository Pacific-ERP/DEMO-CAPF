# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAccount(models.Model):
    _name = 'account.account'
    _inherit = ['account.account', 'mail.thread']

    code = fields.Char(tracking=True)
    name = fields.Char(tracking=True)
    user_type_id = fields.Many2one(tracking=True)
    reconcile = fields.Boolean(tracking=True)