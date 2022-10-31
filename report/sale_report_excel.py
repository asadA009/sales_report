from odoo import models, _


class SalesReportXlsx(models.AbstractModel):
    _name = 'report.sales_report.sales_report_xlsx'
    _description = 'Sales Report XLSX'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        domain = [('date', '>=', date_from),
                  ('date', '<=', date_to)]
        records = self.env["account.move.dynamic"].search(domain)
        title_format = workbook.add_format(
            {'bg_color': '#FFFFFF', 'align': 'center', 'valign': 'vcenter', 'font_size': 25,
             'font_color': 'black'})
        title_format.set_border(2)
        bold_date_format = workbook.add_format(
            {'bg_color': '#FFFFFF', 'align': 'center', 'valign': 'vcenter', 'font_size': 10,
             'bold': True,
             'font_color': 'black'})
        bold_date_format.set_border(2)
        date_format = workbook.add_format(
            {'bg_color': '#FFFFFF', 'align': 'center', 'valign': 'vcenter', 'font_size': 10,
             'font_color': 'black'})
        date_format.set_border(2)
        main_format = workbook.add_format(
            {'bg_color': '#add8e6', 'align': 'center', 'valign': 'vcenter', 'font_size': 22,
             'num_format': '#,##0.00',
             'font_color': 'black'})
        main_format.set_border(2)
        line_format = workbook.add_format(
            {'bg_color': '#FFFFFF', 'align': 'center', 'valign': 'vcenter', 'font_size': 12,
             'num_format': '#,##0.00',
             'font_color': 'black'})
        line_format.set_border(2)
        total_format = workbook.add_format(
            {'bg_color': '#FFFFFF', 'align': 'center', 'valign': 'vcenter', 'font_size': 12,
             'bold': True,
             'num_format': '#,##0.00',
             'font_color': 'black'})
        total_format.set_border(2)

        worksheet = workbook.add_worksheet(_("Managerial Summary"))
        worksheet.merge_range('A2:H3', _("Managerial Summary"), title_format)

        # Date Line
        worksheet.merge_range('A4:B4', _("From Date"), bold_date_format)
        worksheet.merge_range('C4:D4', date_from, date_format)
        worksheet.merge_range('E4:F4', _("To Date"), bold_date_format)
        worksheet.merge_range('G4:H4', date_to, date_format)
        worksheet.merge_range('G4:H4', date_to, date_format)

        # Heading
        worksheet.merge_range('A6:H7', _("Revenues"), main_format)

        #
        # # Normal Lines
        # worksheet.merge_range('A8:D9', _("Managerial Income"), line_format)
        # worksheet.merge_range('E8:H9', round(commission, 2), line_format)
        #
        # worksheet.merge_range('A10:D11', _("Parking Income"), line_format)
        # worksheet.merge_range('E10:H11', round(dispatching_expenses, 2), line_format)
        #
        # worksheet.merge_range('A12:D13', _("Net Income Dispatches"), line_format)
        # worksheet.merge_range('E12:H13', round(net_amount, 2), line_format)
        #
        # worksheet.merge_range('A14:D15', _("Other Income"), line_format)
        # worksheet.merge_range('E14:H15', round(other_income, 2), line_format)
        #
        # # Total Line
        # worksheet.merge_range('A16:D17', _("Total Revenue"), total_format)
        # worksheet.merge_range('E16:H17', round(commission, 2), total_format)
        #
        # # Heading
        # worksheet.merge_range('A18:H19', _("Expenses"), main_format)
        #
        # # Expense Lines
        # line = 20
        # for expense in expenses:
        #     print('A' + str(line) + ':D' + str(line+1))
        #     worksheet.merge_range('A' + str(line) + ':D' + str(line+1), expense['account'], line_format)
        #     worksheet.merge_range('E' + str(line) + ':H' + str(line+1), round(expense['balance'], 2), line_format)
        #     line += 2
        #
        # # Total Line
        # worksheet.merge_range('A' + str(line) + ':D' + str(line+1), _("Total Expenses"), total_format)
        # worksheet.merge_range('E' + str(line) + ':H' + str(line+1), round(total_expenses, 2), total_format)
        # line += 2
        #
        # # Heading Line
        # worksheet.merge_range('A' + str(line) + ':D' + str(line+1), _("Net (P&L)"), main_format)
        # worksheet.merge_range('E' + str(line) + ':H' + str(line+1), round(grand_net, 2), main_format)

        # Check language for RTL
        # lg = self.env['res.lang']._lang_get(self.env.user.lang)
        # if lg.direction == 'rtl':
        #     worksheet.right_to_left()
