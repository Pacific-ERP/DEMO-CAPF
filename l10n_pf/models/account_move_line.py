# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _name = 'account.move.line'
    _inherit = ['account.move.line', 'mail.thread']

    name = fields.Char(tracking=True)
    account_id = fields.Many2one(tracking=True)
    partner_id = fields.Many2one(tracking=True)
    move_id = fields.Many2one(tracking=True)
    debit = fields.Monetary(tracking=True)
    credit = fields.Monetary(tracking=True)
    amount_currency = fields.Monetary(tracking=True)