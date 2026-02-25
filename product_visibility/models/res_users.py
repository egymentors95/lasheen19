from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_category_ids = fields.Many2many(
        'product.category',
        'res_users_product_category_rel', 'user_id',
        'category_id', string='Allowed Product Categories',
        help='Select the product categories that this user is allowed to see. If no categories are selected, the user will have access to all products.')
