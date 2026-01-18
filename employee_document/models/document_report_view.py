from odoo import fields, models, api


class DocumentReportView(models.Model):
    _name = 'document.report.view'
    _description = 'Employee Document Report'

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    department_id = fields.Many2one(comodel_name="hr.department", string="Department")
    job_id = fields.Many2one(comodel_name="hr.job", string="Job")
    company_id = fields.Many2one(comodel_name="res.company", string="Company")
    document_type = fields.Many2one(comodel_name="document.type", string="Document Type")
    issue_date = fields.Date(string="Date of Issue")
