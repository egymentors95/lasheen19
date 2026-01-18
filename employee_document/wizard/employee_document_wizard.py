from odoo import fields, models, api
from odoo.exceptions import UserError


class EmployeeDocumentWizard(models.TransientModel):
    _name = 'employee.document.wizard'
    _description = "Employee Document Wizard"

    employee_ids = fields.Many2many(comodel_name='hr.employee')
    department_ids = fields.Many2many(comodel_name='hr.department')
    job_position_ids = fields.Many2many(comodel_name='hr.job')
    document_type_ids = fields.Many2many(comodel_name='document.type')
    date_from = fields.Date()
    date_to = fields.Date()

    def get_report_data(self):
        combined_data = []

        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise UserError("Date From must be before or equal to Date To.")

        # -------------------------------
        domain = [
            ('issue_date', '>=', self.date_from),
            ('issue_date', '<=', self.date_to),
        ]
        if self.employee_ids:
            domain.append(('employee_id', 'in', self.employee_ids.ids))
        if self.department_ids:
            domain.append(('employee_id.department_id', 'in', self.department_ids.ids))
        if self.job_position_ids:
            domain.append(('employee_id.job_id', 'in', self.job_position_ids.ids))
        if self.document_type_ids:
            domain.append(('document_type_id', 'in', self.document_type_ids.ids))

        lines = self.env['document.type.line'].search(domain)

        # -------------------------------
        for line in lines:
            employee = line.employee_id
            department = line.employee_id.department_id
            job_position = line.employee_id.job_id
            company = line.employee_id.company_id
            document_type = line.document_type_id
            issue_date = line.issue_date

            # -------- Append --------
            combined_data.append({
                'employee': employee.name,
                'department': department.name,
                'job_position': job_position.name,
                'company': company.name,
                'document_type': document_type.name,
                'issue_date': issue_date,
            # _____________ID___________________
                'employee_id': employee.id,
                'department_id': department.id,
                'job_position_id': job_position.id,
                'company_id': company.id,
                'document_type_id': document_type.id,
            })

        return {'combined_data': combined_data}

    def action_create_list_view(self):
        ReportModel = self.env['document.report.view'].sudo()

        # 1️⃣ حذف الداتا القديمة
        ReportModel.search([]).unlink()

        # 2️⃣ جلب الداتا من الـ Wizard
        report_data = self.get_report_data().get('combined_data', [])

        # 3️⃣ تجهيز الداتا للإنشاء
        vals_list = []
        for line in report_data:
            vals_list.append({
                'employee_id': line['employee_id'],
                'department_id': line['department_id'],
                'job_id': line['job_position_id'],
                'company_id': line['company_id'],
                'document_type': line['document_type_id'],
                'issue_date': line['issue_date'],
            })

        # 4️⃣ إنشاء السجلات الجديدة
        if vals_list:
            ReportModel.create(vals_list)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Employee Document Report',
            'res_model': 'employee.document.wizard',
            'view_mode': 'list',
            'target': 'current',
        }

    def action_download_excel(self):
        """فتح رابط لتحميل Excel من الـ Controller مباشرة"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url = f"{base_url}/employee_document/export_excel?wizard_id={self.id}"
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    def action_print_pdf(self):
        """ Generate PDF report and return ir.actions.report """
        return self.env.ref('employee_document.employee_document_pdf_report').report_action(self)
