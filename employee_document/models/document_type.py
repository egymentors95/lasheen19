from odoo import models, fields, api


class DocumentType(models.Model):
    _name = 'document.type'
    _description = 'Document Type'

    name = fields.Char(required=True, string='Name')
    code = fields.Char(required=True, string='Code')
    