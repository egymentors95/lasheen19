from odoo import fields, models, api
from odoo.exceptions import UserError


class SocialInsuranceWizard(models.TransientModel):
    _name = 'social.insurance.wizard'
    _description = "Social Insurance Wizard"

    date_from = fields.Date()
    date_to = fields.Date()
    employee_ids = fields.Many2many(comodel_name='hr.employee')
    department_ids = fields.Many2many(comodel_name='hr.department')
    job_position_ids = fields.Many2many(comodel_name='hr.job')
    job_title_ids = fields.Many2many(comodel_name='job.title')
    insurance_office_ids = fields.Many2many(comodel_name='insurance.office', string='Insurance Office')
    category_ids = fields.Many2many(comodel_name='social.category', string='Category')
    establishment_number = fields.Char(string='Establishment Number')
    insurance_number = fields.Char(string='Insurance Number')

    def get_report_data(self):
        combined_data = []

        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise UserError("Date From must be before or equal to Date To.")

        # -------------------------------
        domain = [
            ('entry_date', '>=', self.date_from),
            ('entry_date', '<=', self.date_to),
        ]
        if self.employee_ids:
            domain.append(('employee_id', 'in', self.employee_ids.ids))
        if self.department_ids:
            domain.append(('employee_id.department_id', 'in', self.department_ids.ids))
        if self.job_position_ids:
            domain.append(('employee_id.job_id', 'in', self.job_position_ids.ids))
        if self.job_title_ids:
            domain.append(('job_title_id', 'in', self.job_title_ids.ids))
        if self.insurance_office_ids:
            domain.append(('insurance_office_id', 'in', self.insurance_office_ids.ids))
        if self.category_ids:
            domain.append(('category_id', 'in', self.category_ids.ids))
        if self.establishment_number:
            domain.append(('establishment_number', '=', self.establishment_number))
        if self.insurance_number:
            domain.append(('insurance_number', '=', self.insurance_number))

        lines = self.env['social.insurance'].search(domain)

        # -------------------------------
        for line in lines:
            employee = line.employee_id
            department = line.employee_id.department_id
            job_position = line.employee_id.job_id
            company = line.employee_id.company_id
            job_title = line.job_title_id
            insurance_office = line.insurance_office_id
            category = line.category_id

            # ____________________________________________________
            insurance_number = line.insurance_number
            establishment_number = line.establishment_number
            entry_date = line.entry_date
            exit_date = line.exit_date
            insurance_amount = line.insurance_amount
            company_portion = line.company_portion
            employee_portion = line.employee_portion
            monthly_obligation = line.monthly_obligation

            # -------- Append --------
            combined_data.append({
                'employee': employee.name,
                'department': department.name,
                'job_position': job_position.name,
                'company': company.name,
                'job_title': job_title.name,
                'insurance_office': insurance_office.name,
                'category': category.name,
                # ___________________________________
                'insurance_number': insurance_number,
                'establishment_number': establishment_number,
                'entry_date': entry_date,
                'exit_date': exit_date,
                'insurance_amount': insurance_amount,
                'company_portion': company_portion,
                'employee_portion': employee_portion,
                'monthly_obligation': monthly_obligation,
                # _____________ID___________________
                'employee_id': employee.id,
                'department_id': department.id,
                'job_id': job_position.id,
                'company_id': company.id,
                'job_title_id': job_title.id,
                'insurance_office_id': insurance_office.id,
                'category_id': category.id,
            })

        return {'combined_data': combined_data}


    def action_download_excel(self):
        """فتح رابط لتحميل Excel من الـ Controller مباشرة"""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url = f"{base_url}/social_insurance/export_excel?wizard_id={self.id}"
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }



    def action_print_pdf(self):
        """ Generate PDF report and return ir.actions.report """
        return self.env.ref('social_insurance.social_insurance_wizard_pdf_report').report_action(self)

    def action_create_list_view(self):
        ReportModel = self.env['social.report.view'].sudo()

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
                'job_id': line['job_id'],
                'company_id': line['company_id'],
                'job_title_id': line['job_title_id'],
                'insurance_office_id': line['insurance_office_id'],
                'category_id': line['category_id'],
                'insurance_number': line['insurance_number'],
                'establishment_number': line['establishment_number'],
                'entry_date': line['entry_date'],
                'exit_date': line['exit_date'],
                'insurance_amount': line['insurance_amount'],
                'company_portion': line['company_portion'],
                'employee_portion': line['employee_portion'],
                'monthly_obligation': line['monthly_obligation'],
            })

        # 4️⃣ إنشاء السجلات الجديدة
        if vals_list:
            ReportModel.create(vals_list)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Social Insurance Report',
            'res_model': 'social.report.view',
            'view_mode': 'list',
            'target': 'current',
        }

