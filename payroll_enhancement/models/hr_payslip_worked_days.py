from odoo import models, fields, api


class HrPayslipWorkedDays(models.Model):
    _inherit = 'hr.payslip.worked_days'

    version_id = fields.Many2one(related='payslip_id.version_id', store=True)
    payslip_run_id = fields.Many2one(related='payslip_id.payslip_run_id', store=True)
    struct_id = fields.Many2one(related='payslip_id.struct_id', store=True)
    work_location_id = fields.Many2one(related='payslip_id.employee_id.work_location_id', store=True)
    date_from = fields.Date(string='From', related="payslip_id.date_from", store=True)
    date_to = fields.Date(string='To', related="payslip_id.date_to", store=True)
