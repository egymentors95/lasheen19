from odoo import models, api, fields


class InsuranceProvider(models.Model):
    _name = 'insurance.provider'
    _description = 'Insurance Provider'

    name = fields.Char(required=True)