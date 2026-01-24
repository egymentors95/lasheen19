from odoo import models, fields, api
from io import BytesIO
import base64
import xlsxwriter

class DocumentTypeLine(models.Model):
    _name = 'document.type.line'
    _description = 'Document Type Line'

    employee_id = fields.Many2one(comodel_name='hr.employee')
    department_id = fields.Many2one(comodel_name='hr.department', related='employee_id.department_id', store=True)
    job_id = fields.Many2one(comodel_name='hr.job', related='employee_id.job_id', store=True)
    company_id = fields.Many2one(comodel_name='res.company', realted='employee_id.company_id', store=True)
    document_type_id = fields.Many2one(comodel_name='document.type', required=True)
    issue_date = fields.Date(required=True)
    name = fields.Char(string="Description")
    excel_file = fields.Binary('Excel File')
    excel_filename = fields.Char('Excel Filename')
    ir_attachment_ids = fields.One2many(comodel_name='ir.attachment', inverse_name='document_type_line_id')
    attachments_count = fields.Integer(string='Attachments Count', compute='_compute_attachments_count')
    true_false = fields.Boolean(string='True/False')


    @api.depends('ir_attachment_ids')
    def _compute_attachments_count(self):
        for rec in self:
            rec.attachments_count = len(rec.ir_attachment_ids)


    def action_view_uploads(self):
        self.ensure_one()

        return {
            'name': 'Uploads',
            'type': 'ir.actions.act_window',
            'res_model': 'ir.attachment',
            'view_mode': 'kanban,list,form',
            'target': 'current',
            'domain': [('id', 'in', self.ir_attachment_ids.ids)],
            'context': {
                'default_res_model': 'document.type.line',
                'default_res_id': self.id,
                'default_type': 'binary',
                'default_name': 'New Attachment',
                'default_document_type_line_id': self.id,
            }
        }

    def generate_excel_report(self):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Employee Documents")

        # ضبط عرض الأعمدة
        sheet.set_column(0, 0, 20)  # Employee
        sheet.set_column(1, 1, 20)  # Department
        sheet.set_column(2, 2, 20)  # Job Position
        sheet.set_column(3, 3, 20)  # Company
        sheet.set_column(4, 4, 25)  # Document Type
        sheet.set_column(5, 5, 15)  # Issue Date

        # تنسيقات
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        cell_format = workbook.add_format({'border': 1})

        # رؤوس الأعمدة
        headers = ['Employee', 'Department', 'Job Position', 'Company', 'Document Type', 'Issue Date']
        for col, header in enumerate(headers):
            sheet.write(0, col, header, header_format)

        # البيانات لكل السجلات
        for row, line in enumerate(self, start=1):
            sheet.write(row, 0, line.employee_id.name or '', cell_format)
        sheet.write(row, 1, line.department_id.name or '', cell_format)
        sheet.write(row, 2, line.job_id.name or '', cell_format)
        sheet.write(row, 3, line.company_id.name or '', cell_format)
        sheet.write(row, 4, line.document_type_id.name or '', cell_format)
        sheet.write(row, 5, str(line.issue_date) or '', cell_format)

        workbook.close()
        output.seek(0)

        # لتخزين الملف على أول سجل فقط (Odoo يحتاج سجل واحد للـ Binary)
        first_record = self[0]
        first_record.excel_file = base64.b64encode(output.read())
        first_record.excel_filename = 'Employee_Documents.xlsx'

        # فتح التحميل مباشرة
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=document.type.line&id=%s&field=excel_file&filename_field=excel_filename&download=true' % (
                first_record.id),
            'target': 'self',
        }