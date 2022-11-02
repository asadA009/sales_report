from odoo import fields, models, _
from odoo.exceptions import UserError


class SalesReportWizard(models.TransientModel):
    _name = 'sales.report.wizard'
    _description = 'Sale Report Wizard'

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    user_id = fields.Many2one("res.users", "Salesperson")

    def print_report(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to
        }
        return self.env.ref('sales_report.report_for_sales').report_action(self, data=data)

    def print_report_xlsx(self):
        if not self.user_id:
            raise UserError(_("You have to select salesperson to extract an EXCEL report!"))
        data = {
            "form": {
                "date_from": self.date_from,
                "date_to": self.date_to,
                "user_id": self.user_id.id
            }
        }
        return self.env.ref('sales_report.action_report_sales_xlsx').report_action(self,
                                                                                   data=data)

    def tree_view(self):
        tree_view_id = self.env.ref('sales_report.account_move_dynamic_tree_view').ids
        domain = [('date', '>=', self.date_from), ('date', '<=', self.date_to)]
        if self.user_id:
            domain += [('user_id', '=', self.user_id.id)]
        return {
            'name': _('Sales Report for Period: ') + f'{self.date_from} - {self.date_to}',
            'view_mode': 'tree',
            'views': [[tree_view_id, 'tree']],
            'res_model': 'account.move.dynamic',
            'type': 'ir.actions.act_window',
            'domain': domain,
            'target': 'current',
        }
