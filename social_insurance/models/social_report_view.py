from odoo import fields, models, api


class SocialReportView(models.Model):
    _name = 'social.report.view'
    _description = 'Social Report'

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    department_id = fields.Many2one(comodel_name="hr.department", string="Department")
    job_id = fields.Many2one(comodel_name="hr.job", string="Job")
    company_id = fields.Many2one(comodel_name="res.company", string="Company")
    job_title_id = fields.Many2one(comodel_name='job.title', string='Job Title')
    insurance_office_id = fields.Many2one(comodel_name='insurance.office', string='Insurance Office')
    category_id = fields.Many2one(comodel_name='social.category', string='Category')
    insurance_number = fields.Char(string='Insurance Number')
    establishment_number = fields.Char(string='Establishment Number')
    entry_date = fields.Datetime(string='Entry Date')
    exit_date = fields.Datetime(string='Exit Date')
    insurance_amount = fields.Monetary(string='Insurance Amount')
    company_portion = fields.Monetary(string='Company Portion')
    employee_portion = fields.Monetary(string='Employee Portion')
    monthly_obligation = fields.Monetary(string='Monthly Obligation', compute='_compute_monthly_obligation', store=True)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)

