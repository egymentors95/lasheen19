from odoo import models, api, fields


class InsuranceCategory(models.Model):
    _name = 'insurance.category'
    _description = 'Insurance Category'

    name = fields.Char(required=True)