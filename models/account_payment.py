from odoo import fields, models, api


class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'

    def _get_invoice_default_sale_team(self):
        return self.env['crm.team']._get_default_team_id()

    team_id = fields.Many2one(
        'crm.team', string='Sales Team', default=_get_invoice_default_sale_team,
        ondelete="set null", tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    user_id = fields.Many2one('res.users', related='partner_id.user_id', string='User', store=True)

    @api.onchange('user_id')
    def onchange_user_id(self):
        if self.user_id and self.user_id.sale_team_id:
            self.team_id = self.env['crm.team']._get_default_team_id(user_id=self.user_id.id,
                                                                     domain=[('company_id', '=', self.company_id.id)])
