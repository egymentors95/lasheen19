from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    document_line_ids = fields.One2many(comodel_name='document.type.line', inverse_name='employee_id')