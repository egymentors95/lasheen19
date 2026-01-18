from odoo import models, api, fields


class InsuranceOffice(models.Model):
    _name = 'insurance.office'
    _description = 'Insurance Office'

    name = fields.Char(required=True)