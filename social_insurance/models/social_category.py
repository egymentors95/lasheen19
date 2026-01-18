from odoo import models, api, fields


class SocialCategory(models.Model):
    _name = 'social.category'
    _description = 'Category'

    name = fields.Char(required=True)