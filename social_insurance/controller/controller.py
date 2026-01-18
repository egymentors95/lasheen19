from odoo import http
from odoo.http import request
import io
import xlsxwriter
import base64


class EmployeeDocumentController(http.Controller):

    @http.route('/social_insurance/export_excel', type='http', auth='user')
    def export_excel(self, wizard_id=None, **kwargs):
        wizard = request.env['social.insurance.wizard'].browse(int(wizard_id))
        data = wizard.get_report_data()
        lines = data.get('combined_data', [])

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Social Insurance')

        # Formats
        header_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'center'})
        text_format = workbook.add_format({'border': 1})

        # Headers
        headers = ['Employee', 'Department', 'Job Position', 'Company', 'Job Title', 'Insurance Office', 'Category',
                   'Insurance Number', 'Establishment Number', 'Entry Date', 'Exit Date', 'Insurance Amount',
                   'Company Portion', 'Employee Portion', 'Monthly Obligation']

        # Write headers
        for col, header in enumerate(headers):
            sheet.write(0, col, header, header_format)

        # Set column widths for readability
        sheet.set_column(0, 0, 25)  # Employee
        sheet.set_column(1, 1, 20)  # Department
        sheet.set_column(2, 2, 20)  # Job Position
        sheet.set_column(3, 3, 25)  # Company
        sheet.set_column(4, 4, 20)  # Document Type
        sheet.set_column(5, 5, 20)  # Issue Date
        sheet.set_column(6, 6, 20)  # Document Type
        sheet.set_column(7, 7, 20)  # Document Type
        sheet.set_column(8, 8, 20)  # Document Type
        sheet.set_column(9, 9, 20)  # Document Type
        sheet.set_column(10, 10, 20)  # Document Type
        sheet.set_column(11, 11, 20)  # Document Type
        sheet.set_column(12, 12, 20)  # Document Type
        sheet.set_column(13, 13, 20)  # Document Type
        sheet.set_column(14, 14, 20)  # Document Type
        sheet.set_column(15, 15, 20)  # Document Type


        # Write data rows
        row = 1
        for line in lines:
            sheet.write(row, 0, line.get('employee', ''), text_format)
            sheet.write(row, 1, line.get('department', ''), text_format)
            sheet.write(row, 2, line.get('job_position', ''), text_format)
            sheet.write(row, 3, line.get('company', ''), text_format)
            sheet.write(row, 4, line.get('job_title', ''), text_format)
            sheet.write(row, 5, line.get('insurance_office', ''), text_format)
            sheet.write(row, 6, line.get('category', ''), text_format)
            sheet.write(row, 7, line.get('insurance_number', ''), text_format)
            sheet.write(row, 8, line.get('establishment_number', ''), text_format)
            sheet.write(row, 9, line.get('entry_date', ''), text_format)
            sheet.write(row, 10, line.get('exit_date', ''), text_format)
            sheet.write(row, 11, line.get('insurance_amount', ''), text_format)
            sheet.write(row, 12, line.get('company_portion', ''), text_format)
            sheet.write(row, 13, line.get('employee_portion', ''), text_format)
            sheet.write(row, 14, line.get('monthly_obligation', ''), text_format)
            row += 1

        workbook.close()
        output.seek(0)
        excel_data = output.read()

        return request.make_response(
            excel_data,
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename="Social_Report.xlsx"')
            ]
        )
