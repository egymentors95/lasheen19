from odoo import models, fields


class FamilyInsuranceConfig(models.Model):
    _name = "family.insurance.config"
    _description = "Family Insurance Config"

    name = fields.Char(string='Name')
    age_from = fields.Integer(string='Minimum Age')
    age_to = fields.Integer(string='Maximum Age')
    company_share= fields.Float(string='Company Share (%)')
    employee_share = fields.Float(string='Employee Share (%)')