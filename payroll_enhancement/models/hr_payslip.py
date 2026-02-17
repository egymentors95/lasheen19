from odoo import api, fields, models


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    work_location_id = fields.Many2one(comodel_name='hr.work.location', string='Work Location', related='employee_id.work_location_id', store=True)