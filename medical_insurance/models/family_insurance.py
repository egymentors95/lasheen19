from odoo import fields, models, api
from io import BytesIO
import base64
import xlsxwriter

class FamilyInsurance(models.Model):
    _name = 'family.insurance'
    _description = 'Family Insurance'


    employee_id = fields.Many2one(comodel_name='hr.employee', string='employee')
    department_id = fields.Many2one(comodel_name='hr.department', related='employee_id.department_id', store=True)
    job_id = fields.Many2one(comodel_name='hr.job', related='employee_id.job_id', store=True)
    company_id = fields.Many2one(comodel_name='res.company', related='employee_id.company_id', store=True)
    registration_number = fields.Char(string='Reference', related='employee_id.registration_number', store=True)
    family_member_name = fields.Char()
    relation_id = fields.Many2one(comodel_name='medical.relation', string='Relation')
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
    excel_file = fields.Binary(string='Excel File')
    excel_filename = fields.Char(string='Excel Filename')
    in_active = fields.Boolean(string='Active/In Active', compute='_get_in_active', store=True)

    @api.depends('insurance_end_date')
    def _get_in_active(self):
        for rec in self:
            today = fields.Date.context_today(rec)
            rec.in_active = not rec.insurance_end_date or rec.insurance_end_date > today


    @api.depends('company_share', 'employee_share')
    def _get_monthly_contribution(self):
        for rec in self:
            rec.monthly_contribution = rec.company_share + rec.employee_share



    def action_export_family_insurance_excel(self):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Family Insurance')

        header_format = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#D9D9D9'
        })
        cell_format = workbook.add_format({'border': 1})

        headers = [
            'Employee',
            'Department',
            'Job',
            'Company',
            'Registration No',
            'Family Member',
            'Relation',
            'Insurance Number',
            'Insurance Provider',
            'Medical Network',
            'Insurance Category',
            'Start Date',
            'End Date',
            'Company Share',
            'Employee Share',
            'Monthly Contribution',
            'Company Discount',
            'Active/In Active',
        ]

        # عرض الأعمدة
        for col in range(len(headers)):
            sheet.set_column(col, col, 20)

        # كتابة الهيدر
        for col, header in enumerate(headers):
            sheet.write(0, col, header, header_format)

        # كتابة البيانات
        row = 1
        for rec in self:
            sheet.write(row, 0, rec.employee_id.name or '', cell_format)
            sheet.write(row, 1, rec.department_id.name or '', cell_format)
            sheet.write(row, 2, rec.job_id.name or '', cell_format)
            sheet.write(row, 3, rec.company_id.name or '', cell_format)
            sheet.write(row, 4, rec.registration_number or '', cell_format)
            sheet.write(row, 5, rec.family_member_name or '', cell_format)
            sheet.write(row, 6, rec.relation_id.name or '', cell_format)
            sheet.write(row, 7, rec.insurance_number or '', cell_format)
            sheet.write(row, 8, rec.insurance_provider_id.name or '', cell_format)
            sheet.write(row, 9, rec.medical_network_id.name or '', cell_format)
            sheet.write(row,10, rec.insurance_category_id.name or '', cell_format)
            sheet.write(row,11, rec.insurance_start_date or '', cell_format)
            sheet.write(row,12, rec.insurance_end_date or '', cell_format)
            sheet.write(row,13, rec.company_share or 0, cell_format)
            sheet.write(row,14, rec.employee_share or 0, cell_format)
            sheet.write(row,15, rec.monthly_contribution or 0, cell_format)
            sheet.write(row,16, rec.company_discount or 0, cell_format)
            sheet.write(row,17, rec.in_active or 0, cell_format)
            row += 1

        workbook.close()
        output.seek(0)

        self.excel_file = base64.b64encode(output.read())
        self.excel_filename = 'Family_Insurance_Report.xlsx'

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=family.insurance'
                   '&ids=%s'
                   '&field=excel_file'
                   '&filename_field=excel_filename'
                   '&download=true' % (','.join(map(str, self.ids))),
            'target': 'self',
        }