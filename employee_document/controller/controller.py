from odoo import http
from odoo.http import request
import io
import xlsxwriter
import base64

class EmployeeDocumentController(http.Controller):

    @http.route('/employee_document/export_excel', type='http', auth='user')
    def export_excel(self, wizard_id=None, **kwargs):
        wizard = request.env['employee.document.wizard'].browse(int(wizard_id))
        data = wizard.get_report_data()
        lines = data.get('combined_data', [])

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Employee Documents')

        # Formats
        header_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'center'})
        text_format = workbook.add_format({'border': 1})

        # Headers
        headers = ['Employee','Department','Job Position','Company','Document Type','Issue Date']

        # Write headers
        for col, header in enumerate(headers):
            sheet.write(0, col, header, header_format)

        # Set column widths for readability
        sheet.set_column(0, 0, 25)  # Employee
        sheet.set_column(1, 1, 20)  # Department
        sheet.set_column(2, 2, 20)  # Job Position
        sheet.set_column(3, 3, 25)  # Company
        sheet.set_column(4, 4, 20)  # Document Type
        sheet.set_column(5, 5, 15)  # Issue Date

        # Write data rows
        row = 1
        for line in lines:
            sheet.write(row, 0, line.get('employee', ''), text_format)
            sheet.write(row, 1, line.get('department', ''), text_format)
            sheet.write(row, 2, line.get('job_position', ''), text_format)
            sheet.write(row, 3, line.get('company', ''), text_format)
            sheet.write(row, 4, line.get('document_type', ''), text_format)
            sheet.write(row, 5, str(line.get('issue_date', '')), text_format)
            row += 1

        workbook.close()
        output.seek(0)
        excel_data = output.read()

        return request.make_response(
            excel_data,
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename="Employee_Documents.xlsx"')
            ]
        )
