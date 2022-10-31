from odoo import fields, models, tools

RECORD_TYPE = [('out_invoice', 'Regular Invoice'),
               ('out_refund', 'Credit Note'),
               ('inbound', 'Customer Payment'),
               ('outbound', 'Customer Refund')]


class AccountMoveDynamic(models.Model):
    _name = 'account.move.dynamic'
    _description = 'SQL view'
    _auto = False

    name = fields.Char(string='Name')
    date = fields.Date(string='Date')
    move_type = fields.Selection(RECORD_TYPE)
    amount = fields.Float(string='Amount')
    journal_id = fields.Many2one('account.journal')
    user_id = fields.Many2one('res.users', string='SalesPerson')
    team_id = fields.Many2one('crm.team', string='Team')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, "account_move_dynamic")
        self._cr.execute("""
        CREATE or REPLACE view account_move_dynamic AS (
        select act.id AS id,
        act.name AS name,
        CASE WHEN act.payment_id IS NOT NULL THEN pay.payment_type ELSE act.move_type END AS move_type,
        act.journal_id AS journal_id,
        act.date AS date,
        CASE WHEN act.payment_id IS NOT NULL THEN pay.user_id ELSE act.invoice_user_id END AS user_id,
        CASE WHEN act.payment_id IS NOT NULL THEN pay.team_id ELSE act.team_id END AS team_id,
        pay.payment_type AS payment_type,
        CASE 
        WHEN act.payment_id IS NOT NULL AND pay.payment_type = 'outbound'
        THEN 0 - act.amount_total_signed
        WHEN act.payment_id IS NOT NULL AND pay.payment_type = 'inbound'
        THEN act.amount_total_signed
        ELSE act.amount_total_signed END AS amount
        FROM account_move AS act LEFT JOIN account_payment AS pay ON act.payment_id = pay.id
        WHERE (act.payment_id IS NOT NULL OR act.move_type IN ('out_invoice', 'out_refund')) AND act.state = 'posted'
        )""")
