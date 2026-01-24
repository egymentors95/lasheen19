from odoo import fields, models, api
import xlsxwriter
from io import BytesIO
import base64

class MedicalInsurance(models.Model):
    _name = 'medical.insurance'
    _description = 'Medical Insurance'

    employee_id = fields.Many2one(comodel_name='hr.employee', string='employee')
    department_id = fields.Many2one(comodel_name='hr.department', related='employee_id.department_id', store=True)
    job_id = fields.Many2one(comodel_name='hr.job', related='employee_id.job_id', store=True)
    company_id = fields.Many2one(comodel_name='res.company', realted='employee_id.company_id', store=True)
    registration_number = fields.Char(string='Reference', related='employee_id.registration_number', store=True)
    insurance_number = fields.Char(string='Insurance Number')
    insurance_provider_id = fields.Many2one(comodel_name='insurance.provider', string='Insurance Provider')
    medical_network_id = fields.Many2one(comodel_name='medical.network', string='Medical Network')
    insurance_category_id = fields.Many2one(comodel_name='insurance.category', string='Insurance Category')
    insurance_start_date = fields.Date(string='Insurance Start Date')
    insurance_end_date = fields.Date(string='Insurance End Date')
    company_share = fields.Float(string='Company Share')
    employee_share = fields.Float(string='Employee Share')
    monthly_contribution = fields.Float(string='Monthly Contribution', compute='_get_monthly_contribution', store=True)
    company_discount = fields.Float()

    excel_file = fields.Binary('Excel File')
    excel_filename = fields.Char('Excel Filename')

    @api.depends('company_share', 'employee_share')
    def _get_monthly_contribution(self):
        for rec in self:
            rec.monthly_contribution = rec.company_share + rec.employee_share


    def generate_excel_report_multiple(self):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Medical Insurance")

        # إعداد أعمدة بعرض مناسب
        columns = [
            ('Employee', 20),
            ('Department', 20),
            ('Job', 20),
            ('Reference', 20),
            ('Insurance Number', 20),
            ('Insurance Provider', 20),
            ('Medical Network', 20),
            ('Insurance Category', 20),
            ('Start Date', 20),
            ('End Date', 20),
            ('Company Share', 15),
            ('Employee Share', 15),
            ('Monthly Contribution', 15),
            ('Company Discount', 15)
        ]
        for col, (header, width) in enumerate(columns):
            sheet.set_column(col, col, width)

        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        cell_format = workbook.add_format({'border': 1})

        # كتابة رؤوس الأعمدة
        for col, (header, _) in enumerate(columns):
            sheet.write(0, col, header, header_format)

        # كتابة البيانات لكل السجلات
        for row, record in enumerate(self, start=1):
            sheet.write(row, 0, record.employee_id.name or '', cell_format)
            sheet.write(row, 1, record.department_id.name or '', cell_format)
            sheet.write(row, 2, record.job_id.name or '', cell_format)
            sheet.write(row, 3, record.registration_number or '', cell_format)
            sheet.write(row, 4, record.insurance_number or '', cell_format)
            sheet.write(row, 5, record.insurance_provider_id.name or '', cell_format)
            sheet.write(row, 6, record.medical_network_id.name or '', cell_format)
            sheet.write(row, 7, record.insurance_category_id.name or '', cell_format)
            sheet.write(row, 8, str(record.insurance_start_date) or '', cell_format)
            sheet.write(row, 9, str(record.insurance_end_date) or '', cell_format)
            sheet.write(row, 10, record.company_share or 0, cell_format)
            sheet.write(row, 11, record.employee_share or 0, cell_format)
            sheet.write(row, 12, record.monthly_contribution or 0, cell_format)
            sheet.write(row, 13, record.company_discount or 0, cell_format)

        workbook.close()
        output.seek(0)

        self.excel_file = base64.b64encode(output.read())
        self.excel_filename = 'Medical_Insurance.xlsx'

        # فتح التحميل مباشرة
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=medical.insurance&ids=%s&field=excel_file&filename_field=excel_filename&download=true' % (','.join(str(r.id) for r in self)),
            'target': 'self',
        }