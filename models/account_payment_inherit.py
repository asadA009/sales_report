from odoo import fields, models, api


class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'
    _description = 'Account Payment Inherit'

    partner_id = fields.Many2one('res.partner', string='Partner')
    user_id = fields.Many2one('res.users', related='partner_id.user_id', string='User', store=True)
