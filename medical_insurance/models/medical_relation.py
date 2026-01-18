from odoo import models, api, fields


class MedicalRelation(models.Model):
    _name = 'medical.relation'
    _description = 'Medical Relation'

    name = fields.Char(required=True)