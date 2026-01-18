from odoo import models, api, fields


class MedicalNetwork(models.Model):
    _name = 'medical.network'
    _description = 'Medical Network'

    name = fields.Char(required=True)