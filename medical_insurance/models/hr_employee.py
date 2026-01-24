from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    medical_insurance_ids = fields.One2many(comodel_name='medical.insurance', inverse_name='employee_id')
    family_insurance_ids = fields.One2many(comodel_name='family.insurance', inverse_name='employee_id')