from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    allowed_user_ids = fields.Many2many(
        'res.users',
        'res_users_product_category_rel', 'category_id',
        'user_id', string='Allowed Users',
        help='Select the users that are allowed to see products in this category. If no users are selected, all users will have access to products in this category.')
