from odoo import models, fields, api


class DocumentTypeLine(models.Model):
    _name = 'document.type.line'
    _description = 'Document Type Line'

    employee_id = fields.Many2one(comodel_name='hr.employee')
    document_type_id = fields.Many2one(comodel_name='document.type', required=True)
    issue_date = fields.Date(required=True)
    name = fields.Char(string="Description")
    uploads = fields.Many2many(comodel_name='ir.attachment')