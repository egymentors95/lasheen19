from odoo.exceptions import ValidationError
from odoo import models, fields, api
from io import BytesIO
import base64
import xlsxwriter


class SocialInsurance(models.Model):
    _name = 'social.insurance'
    _description = 'Social Insurance'

    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    department_id = fields.Many2one(comodel_name='hr.department', related='employee_id.department_id', store=True)
    job_id = fields.Many2one(comodel_name='hr.job', related='employee_id.job_id', store=True)
    company_id = fields.Many2one(comodel_name='res.company', related='employee_id.company_id', readonly=True)
    job_title_id = fields.Many2one(comodel_name='job.title', string='Job Title')
    insurance_office_id = fields.Many2one(comodel_name='insurance.office', string='Insurance Office')
    category_id = fields.Many2one(comodel_name='social.category', string='Category')
    insurance_number = fields.Char(string='Insurance Number')
    establishment_number = fields.Char(string='Establishment Number')
    entry_date = fields.Date(string='Entry Date')
    exit_date = fields.Date(string='Exit Date')
    in_active = fields.Boolean(string='Active/In Active', compute='_get_in_active', store=True)
    insurance_amount = fields.Monetary(string='Insurance Amount')
    company_portion = fields.Monetary(string='Company Portion', compute='_get_company_portion', store=True)
    employee_portion = fields.Monetary(string='Employee Portion', compute='_get_employee_portion', store=True)
    monthly_obligation = fields.Monetary(string='Monthly Obligation', compute='_compute_monthly_obligation', store=True)

    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    excel_file = fields.Binary('Excel File')
    excel_filename = fields.Char('Excel Filename')

    @api.depends('insurance_amount', 'employee_id', 'employee_id.age', 'employee_id.birthday')
    def _get_company_portion(self):
        social_insurance_config = self.env['social.insurance.config'].search([
            ('age_from', '<=', self.employee_id.age),
            ('age_to', '>=', self.employee_id.age),
        ], limit=1)
        company_contribution = social_insurance_config.company_contribution if social_insurance_config else 0
        for rec in self:
            if rec.insurance_amount:
                rec.company_portion = rec.insurance_amount * (company_contribution / 100)
            else:
                rec.company_portion = 0


    @api.depends('insurance_amount', 'employee_id', 'employee_id.age', 'employee_id.birthday')
    def _get_employee_portion(self):
        social_insurance_config = self.env['social.insurance.config'].search([
            ('age_from', '<=', self.employee_id.age),
            ('age_to', '>=', self.employee_id.age),
        ], limit=1)
        employee_contribution = social_insurance_config.employee_contribution if employee_contribution else 0
        for rec in self:
            if rec.insurance_amount:
                rec.employee_portion = rec.insurance_amount * (employee_contribution / 100)
            else:
                rec.employee_portion = 0

    @api.depends('exit_date')
    def _get_in_active(self):
        for rec in self:
            today = fields.Date.context_today(rec)
            rec.in_active = not rec.exit_date or rec.exit_date > today

    @api.depends('company_portion', 'employee_portion')
    def _compute_monthly_obligation(self):
        for rec in self:
            rec.monthly_obligation = rec.company_portion + rec.employee_portion

    @api.constrains('entry_date', 'exit_date')
    def _check_exit_date(self):
        for record in self:
            if record.entry_date and record.exit_date:
                if record.exit_date < record.entry_date:
                    raise ValidationError(
                        ('Exit Date cannot be earlier than Entry Date.'))

    def generate_excel_report_multiple(self):
        if not self:
            return

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Social Insurance")

        # تنسيقات
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        cell_format = workbook.add_format({'border': 1})

        # رؤوس الأعمدة
        headers = [
            'Employee', 'Department', 'Job Position', 'Company', 'Job Title', 'Insurance Office', 'Category',
            'Insurance Number', 'Establishment Number', 'Entry Date', 'Exit Date',
            'Insurance Amount', 'Company Portion', 'Employee Portion', 'Monthly Obligation', 'Active/In Active'
        ]
        for col, header in enumerate(headers):
            sheet.write(0, col, header, header_format)
            sheet.set_column(col, col, 18)  # تكبير مساحة الأعمدة

        # البيانات لكل السجلات المحددة
        for row, line in enumerate(self, start=1):
            sheet.write(row, 0, line.employee_id.name or '', cell_format)
            sheet.write(row, 1, line.department_id.name or '', cell_format)
            sheet.write(row, 2, line.job_id.name or '', cell_format)
            sheet.write(row, 3, line.company_id.name or '', cell_format)
            sheet.write(row, 4, line.job_title_id.name or '', cell_format)
            sheet.write(row, 5, line.insurance_office_id.name or '', cell_format)
            sheet.write(row, 6, line.category_id.name or '', cell_format)
            sheet.write(row, 7, line.insurance_number or '', cell_format)
            sheet.write(row, 8, line.establishment_number or '', cell_format)
            sheet.write(row, 9, str(line.entry_date) or '', cell_format)
            sheet.write(row, 10, str(line.exit_date) or '', cell_format)
            sheet.write(row, 11, line.insurance_amount or 0, cell_format)
            sheet.write(row, 12, line.company_portion or 0, cell_format)
            sheet.write(row, 13, line.employee_portion or 0, cell_format)
            sheet.write(row, 14, line.monthly_obligation or 0, cell_format)
            sheet.write(row, 15, line.in_active or 0, cell_format)

        workbook.close()
        output.seek(0)

        # نحفظ الملف على أول سجل فقط للتحميل
        first_record = self[0]
        first_record.excel_file = base64.b64encode(output.read())
        first_record.excel_filename = 'Social_Insurance.xlsx'

        # نرجع الرابط لتحميل Excel
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=social.insurance&id=%s&field=excel_file&filename_field=excel_filename&download=true' % (
                first_record.id),
            'target': 'self',
        }