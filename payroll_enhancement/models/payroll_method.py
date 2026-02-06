from odoo import models, fields


class PayrollMethod(models.Model):
    _name = 'payroll.method'
    _description = 'Payroll Method'

    name = fields.Char(string='Method Name', required=True)
