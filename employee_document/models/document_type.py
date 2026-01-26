from odoo import models, fields, api


class DocumentType(models.Model):
    _name = 'document.type'
    _description = 'Document Type'

    name = fields.Char(required=True, string='Name')
    code = fields.Char(required=False, string='Code')
    is_active = fields.Boolean(default=True)

    # @api.model
    # def create(self, vals):
    #     record = super().create(vals)
    #     employees = self.env['hr.employee'].search([])
    #
    #     lines = []
    #     for emp in employees:
    #         lines.append({
    #             'employee_id': emp.id,
    #             'document_type_id': record.id,
    #             'issue_date': fields.Date.today(),
    #             'name': record.name,
    #         })
    #
    #     self.env['document.type.line'].create(lines)
    #     return record