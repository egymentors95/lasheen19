from odoo import models, api, fields


class JobTitle(models.Model):
    _name = 'job.title'
    _description = 'Job Title'

    name = fields.Char(required=True)