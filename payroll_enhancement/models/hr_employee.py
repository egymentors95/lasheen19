from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_income_tax_applicable = fields.Boolean(string="Income Tax Applicable", default=False)
    payroll_pay_method_id = fields.Many2one(comodel_name='payroll.method', string="Payroll Pay Method")