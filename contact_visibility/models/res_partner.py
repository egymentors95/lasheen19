from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    allowed_user_ids = fields.Many2many('res.users', 'res_users_res_partner_rel', 'partner_id', 'user_id',
                                        string='Allowed Users')
    is_customer = fields.Boolean(string='Is a Customer')
    is_vendor = fields.Boolean(string='Is a Vendor')
    is_employee = fields.Boolean(string='Is an Employee')
