from odoo import models, fields


class SocialInsuranceConfig(models.Model):
    _name = "social.insurance.config"
    _description = "Social Insurance Config"

    name = fields.Char(string='Name')
    age_from = fields.Integer(string='Minimum Age')
    age_to = fields.Integer(string='Maximum Age')
    company_contribution = fields.Float(string='Company Contribution (%)')
    employee_contribution = fields.Float(string='Employee Contribution (%)')