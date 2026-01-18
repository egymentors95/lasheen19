from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    social_insurance_ids = fields.One2many(comodel_name='social.insurance', inverse_name='employee_id')