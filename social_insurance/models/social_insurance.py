from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SocialInsurance(models.Model):
    _name = 'social.insurance'
    _description = 'Social Insurance'


    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    insurance_number = fields.Char(string='Insurance Number')
    job_title_id = fields.Many2one(comodel_name='job.title', string='Job Title')
    establishment_number = fields.Char(string='Establishment Number')
    insurance_office_id = fields.Many2one(comodel_name='insurance.office', string='Insurance Office')
    entry_date = fields.Datetime(string='Entry Date')
    exit_date = fields.Datetime(string='Exit Date')
    insurance_amount = fields.Monetary(string='Insurance Amount')
    company_portion = fields.Monetary(string='Company Portion')
    employee_portion = fields.Monetary(string='Employee Portion')
    monthly_obligation = fields.Monetary(string='Monthly Obligation', compute='_compute_monthly_obligation', store=True)
    category_id = fields.Many2one(comodel_name='social.category', string='Category')

    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    company_id = fields.Many2one(comodel_name='res.company', related='employee_id.company_id', readonly=True)

    @api.depends('company_portion', 'employee_portion')
    def _compute_monthly_obligation(self):
        for rec in self:
            rec.monthly_obligation = rec.company_portion + rec.employee_portion


    @api.constrains('entry_date', 'exit_date')
    def _check_exit_date(self):
        for record in self:
            if record.entry_date and record.exit_date:
                if record.exit_date < record.entry_date:
                    raise ValidationError(
                        ('Exit Date cannot be earlier than Entry Date.'))

