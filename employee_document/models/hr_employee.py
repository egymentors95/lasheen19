from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    document_line_ids = fields.One2many(comodel_name='document.type.line', inverse_name='employee_id')

    @api.model
    def create(self, vals):
        employee = super(HrEmployee, self).create(vals)

        document_types = self.env['document.type'].search([
            ('is_active', '=', True)
        ])

        lines_vals = []
        for doc_type in document_types:
            lines_vals.append({
                'employee_id': employee.id,
                'document_type_id': doc_type.id,
                'issue_date': fields.Date.today(),
                'name': doc_type.name,
            })

        if lines_vals:
            self.env['document.type.line'].create(lines_vals)

        return employee
