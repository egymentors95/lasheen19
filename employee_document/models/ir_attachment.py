from odoo import models, fields, api


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'


    document_type_line_id = fields.Many2one(comodel_name='document.type.line',)