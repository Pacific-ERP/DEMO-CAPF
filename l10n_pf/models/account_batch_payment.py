# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountBatchPayment(models.Model):
    _name = 'account.batch.payment'
    _inherit = ['account.batch.payment', 'mail.thread']

    batch_type = fields.Selection(tracking=True)
    payment_method_id = fields.Many2one(tracking=True)