from odoo import models, fields


class MedicalInsuranceConfig(models.Model):
    _name = "medical.insurance.config"
    _description = "Medical Insurance Config"

    name = fields.Char(string='Name')
    age_from = fields.Integer(string='Minimum Age')
    age_to = fields.Integer(string='Maximum Age')
    company_share= fields.Float(string='Company Share (%)')
    employee_share = fields.Float(string='Employee Share (%)')