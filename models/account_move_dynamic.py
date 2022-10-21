from odoo import api, fields, models, tools, _

TYPE = [('out_invoice', 'Regular Invoice'),
        ('out_refund', 'Credit Note'),
        ('inbound', 'Customer Payment'),
        ('outbound', 'Customer Refund')]


class AccountMoveDynamic(models.Model):
    _name = 'account.move.dynamic'
    _description = 'SQL view'
    _auto = False

    name = fields.Char(string='Name')
    date = fields.Date(string='Date')
    type = fields.Selection(TYPE)
    amount = fields.Float(string='Amount')
    journal_id = fields.Many2one('account.journal')
    invoice_user_id = fields.Many2one('res.users', string='SalesPerson')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, "account_move_dynamic")
        self._cr.execute("""
        
        CREATE or REPLACE view account_move_dynamic as (

            select act.id as id,
            act.name as name,
            act.journal_id as journal_id,
            act.date as date,
            act.invoice_user_id as invoice_user_id,
                pay.payment_type as type,
                pay.amount as amount
                from account_move as act join account_payment as pay on act.payment_id = pay.id
                )

         """)
