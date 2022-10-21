from odoo import fields, models, api


class SalesReportWizard(models.TransientModel):
    _name = 'sales.report.wizard'
    _description = 'Sale Report Wizard'

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def print_report(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to
        }
        return self.env.ref('sales_report.report_for_sales').report_action(self, data=data)

    def tree_view(self):
        tree_view_id = self.env.ref('sales_report.account_move_dynamic_tree_view').ids
        # form_view_id = self.env.ref('sales_report.account_move_dynamic_form_view').ids
        return {
            'name': 'Test',
            'view_mode': 'tree',
            'views': [[tree_view_id, 'tree']],
            'res_model': 'account.move.dynamic',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }