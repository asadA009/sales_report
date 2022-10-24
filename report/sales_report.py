from odoo import fields, models, api


class SalesReport(models.AbstractModel):
    _name = 'report.sales_report.sales_report_template'
    _description = 'Sales Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        sales_report = self.env['account.move.dynamic'].search(
            [('date', '>=', data['date_from']), ('date', '<=', data['date_to'])])
        return {
            'docs': sales_report,
        }
