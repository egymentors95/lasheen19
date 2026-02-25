from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    allowed_user_ids = fields.Many2many('res.users', 'res_users_res_partner_rel', 'partner_id', 'user_id',
                                        string='Allowed Users')
    contact_type = fields.Selection([
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('employee', 'Employee'),
        ], string='Contact Type')
