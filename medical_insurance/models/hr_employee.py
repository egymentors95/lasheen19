from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    medical_insurance_ids = fields.One2many(comodel_name='medical.insurance', inverse_name='employee_id')
    family_insurance_ids = fields.One2many(comodel_name='family.insurance', inverse_name='employee_id')

    total_company_share = fields.Float(string='Total Company Share', compute='_get_total_company_share', store=True)
    total_employee_share = fields.Float(compute='_get_total_employee_share', store=True, string='Total Employee_share')
    total_monthly_contribution = fields.Float(compute='_get_total_monthly_contribution', store=True,
                                              string='Total Monthly Contribution')
    age = fields.Integer('Age', compute='_compute_age', store=True)

    @api.depends('birthday')
    def _compute_age(self):
        today = fields.Date.today()
        for rec in self:
            if rec.birthday:
                rec.age = today.year - rec.birthday.year - (
                        (today.month, today.day) < (rec.birthday.month, rec.birthday.day)
                )
            else:
                rec.age = 0

    @api.depends('medical_insurance_ids', 'medical_insurance_ids.company_share', 'family_insurance_ids',
                 'family_insurance_ids.company_share')
    def _get_total_company_share(self):
        for rec in self:
            medical_company_share = sum(rec.medical_insurance_ids.mapped('company_share'))
            family_company_share = sum(rec.family_insurance_ids.mapped('company_share'))
            rec.total_company_share = medical_company_share + family_company_share

    @api.depends('medical_insurance_ids', 'medical_insurance_ids.employee_share', 'family_insurance_ids',
                 'family_insurance_ids.employee_share')
    def _get_total_employee_share(self):
        for rec in self:
            medical_employee_share = sum(rec.medical_insurance_ids.mapped('employee_share'))
            family_employee_share = sum(rec.family_insurance_ids.mapped('employee_share'))
            rec.total_employee_share = medical_employee_share + family_employee_share

    @api.depends('medical_insurance_ids', 'medical_insurance_ids.monthly_contribution', 'family_insurance_ids',
                 'family_insurance_ids.monthly_contribution')
    def _get_total_monthly_contribution(self):
        for rec in self:
            medical_monthly_contribution = sum(rec.medical_insurance_ids.mapped('monthly_contribution'))
            family_monthly_contribution = sum(rec.family_insurance_ids.mapped('monthly_contribution'))
            rec.total_monthly_contribution = medical_monthly_contribution + family_monthly_contribution
