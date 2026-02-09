from odoo import models, fields, api


class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'

    employee_id = fields.Many2one(related='slip_id.employee_id', string='Employee', store=True, comodel_name='hr.employee')
    work_location_id = fields.Many2one(comodel_name='hr.work.location', string='Work Location', related='slip_id.work_location_id', store=True)
    payslip_run_id = fields.Many2one(related='slip_id.payslip_run_id', string='Payslip Run', store=True, comodel_name='hr.payslip.run')
    employer_cost = fields.Monetary(string='Employer Cost', related='slip_id.employer_cost', store=True)
    currency_id = fields.Many2one(related='slip_id.currency_id', string='Currency', store=True, comodel_name='res.currency')
    basic_wage = fields.Monetary(string='Basic Wage', related='slip_id.basic_wage', store=True)
    gross_wage = fields.Monetary(string='Gross Wage', related='slip_id.gross_wage', store=True)
    net_wage = fields.Monetary(string='Net Wage', related='slip_id.net_wage', store=True)
    state_display = fields.Selection(related='slip_id.state_display', string='Payslip State', store=True)
    version_id = fields.Many2one(related='slip_id.version_id', store=True)
    struct_id = fields.Many2one(related='slip_id.struct_id', store=True)
    date_from = fields.Date(string='From', related="slip_id.date_from", store=True)
    date_to = fields.Date(string='To', related="slip_id.date_to", store=True)

