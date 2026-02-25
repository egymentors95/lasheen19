from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_partner_ids = fields.Many2many('res.partner', 'res_users_res_partner_rel', 'user_id', 'partner_id',
                                           string='Allowed Partners')