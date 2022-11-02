from odoo import models, _


class SalesReportXlsx(models.AbstractModel):
    _name = 'report.sales_report.sales_report_xlsx'
    _description = 'Sales Report XLSX'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        user_id = data['form']['user_id']
        salesperson_id = self.env["res.partner"].browse(user_id)
        domain = [('date', '>=', date_from),
                  ('date', '<=', date_to)]
        if user_id:
            domain += [('user_id', '=', user_id)]

        records = self.env["account.move.dynamic"].search(domain)

        title_format = workbook.add_format(
            {'bg_color': '#ffc000', 'align': 'center', 'valign': 'vcenter', 'font_size': 10,
             'bold': True,
             'font_color': 'black'})
        title_format.set_bottom(2)
        regular_format = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'font_size': 10,
             'num_format': '#,##0.00',
             'font_color': 'black'})
        regular_format.set_border(1)

        regular_format_borderless = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'font_size': 10,
             'num_format': '#,##0.00',
             'font_color': 'black'})

        summary_format = workbook.add_format(
            {'align': 'left', 'valign': 'vcenter', 'font_size': 10,
             'num_format': '#,##0.00',
             'font_color': 'black'}
        )
        summary_format.set_bottom(2)

        total_format = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'font_size': 10,
             'bold': True,
             'num_format': '#,##0.00',
             'font_color': 'black'})

        total_format.set_bottom(6)
        total_format.set_top(2)

        worksheet = workbook.add_worksheet(_("Sales Report"))

        worksheet.set_column(0, 6, 15)

        worksheet.write(0, 0, 'Sales Rep. Name', regular_format_borderless)
        worksheet.write(1, 0, 'Sales Rep. No.', regular_format_borderless)
        worksheet.write(0, 1, salesperson_id.name, regular_format_borderless)
        worksheet.write(1, 1, salesperson_id.ref or '', regular_format_borderless)

        # Table headings
        worksheet.write(2, 0, "Date", title_format)
        worksheet.write(2, 1, "Ref. No.", title_format)
        worksheet.write(2, 2, "Address", title_format)
        worksheet.write(2, 3, "Warehouse", title_format)
        worksheet.write(2, 4, "Type", title_format)
        worksheet.write(2, 5, "Payment Method", title_format)
        worksheet.write(2, 6, "Amount", title_format)

        total_sales = 0.0

        # Lines
        line = 3
        for record in records:
            document_type = dict(
                self.env['account.move.dynamic']._fields['move_type']._description_selection(self.env)).get(
                record.move_type)
            worksheet.write(line, 0, record.date.strftime("%Y-%m-%d"), regular_format)
            worksheet.write(line, 1, record.name, regular_format)
            worksheet.write(line, 2, "", regular_format)
            worksheet.write(line, 3, "", regular_format)
            worksheet.write(line, 4, document_type, regular_format)
            worksheet.write(line, 5, record.journal_id.name, regular_format)
            worksheet.write(line, 6, record.amount, regular_format)
            total_sales += record.amount
            line += 1

        # Total Line
        worksheet.write(line, 6, total_sales, total_format)
        line += 1
        worksheet.write(line, 0, "Summary", summary_format)

        # Totals
        total_cash_sales = records.filtered(lambda rec:
                                            rec.journal_id.type == 'cash' and rec.move_type == 'inbound')
        total_cash_sales = abs(sum(total_cash_sales.mapped("amount")))

        total_bank_sales = records.filtered(lambda rec:
                                            rec.journal_id.type == 'bank' and rec.move_type == 'inbound')
        total_bank_sales = abs(sum(total_bank_sales.mapped("amount")))

        total_credit_sales = records.filtered(lambda rec:
                                              rec.journal_id.type == 'sale' and rec.move_type == 'out_invoice')
        total_credit_sales = abs(sum(total_credit_sales.mapped("amount"))) - total_bank_sales - total_cash_sales

        total_cash_returns = records.filtered(lambda rec:
                                              rec.journal_id.type == 'cash' and rec.move_type == 'outbound')
        total_cash_returns = sum(total_cash_returns.mapped("amount"))

        total_bank_returns = records.filtered(lambda rec:
                                              rec.journal_id.type == 'bank' and rec.move_type == 'outbound')
        total_bank_returns = sum(total_bank_returns.mapped("amount"))

        total_credit_returns = records.filtered(lambda rec:
                                                rec.journal_id.type == 'sale' and rec.move_type == 'out_refund')
        total_credit_returns = total_bank_returns + total_cash_returns + sum(
            total_credit_returns.mapped("amount")) - total_bank_returns - total_cash_returns

        # Bottom Details
        line += 1
        worksheet.write(line, 0, "Cash Sales", regular_format_borderless)
        worksheet.write(line, 1, round(total_cash_sales, 2), regular_format_borderless)
        worksheet.write(line, 2, "Cash Returns", regular_format_borderless)
        worksheet.write(line, 3, round(total_cash_returns, 2), regular_format_borderless)
        worksheet.write(line, 4, "Net Cash Sales", regular_format_borderless)
        worksheet.write(line, 5, round(total_cash_sales + total_cash_returns, 2), regular_format_borderless)
        line += 1
        worksheet.write(line, 0, "Bank Sales", regular_format_borderless)
        worksheet.write(line, 1, round(total_bank_sales, 2), regular_format_borderless)
        worksheet.write(line, 2, "Bank Returns", regular_format_borderless)
        worksheet.write(line, 3, round(total_bank_returns, 2), regular_format_borderless)
        worksheet.write(line, 4, "Net Bank Sales", regular_format_borderless)
        worksheet.write(line, 5, round(total_bank_sales + total_bank_returns, 2), regular_format_borderless)
        line += 1
        worksheet.write(line, 0, "Credit Sales", regular_format_borderless)
        worksheet.write(line, 1, round(total_credit_sales, 2), regular_format_borderless)
        worksheet.write(line, 2, "Credit Sales Returns", regular_format_borderless)
        worksheet.write(line, 3, round(total_credit_returns, 2), regular_format_borderless)
        worksheet.write(line, 4, "Net Credit Sales", regular_format_borderless)
        worksheet.write(line, 5, round(total_credit_sales + total_credit_returns, 2), regular_format_borderless)
        line += 1
        worksheet.write(line, 0, "Totals", regular_format_borderless)
        worksheet.write(line, 1, round(sum([total_credit_sales, total_bank_sales, total_cash_sales]), 2), total_format)
        worksheet.write(line, 3, round(sum([total_cash_returns, total_bank_returns, total_credit_returns]), 2),
                        total_format)
        worksheet.write(line, 5, round(
            sum([total_cash_sales + total_cash_returns, total_bank_sales + total_bank_returns,
                 total_credit_sales + total_credit_returns]), 2), total_format)
