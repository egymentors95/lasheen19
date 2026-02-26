from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_category_visibility = fields.Boolean(string='Category Visibility', default=False,
                                           help='Check this box to enable category-based visibility for this product. If enabled, the product will only be visible to users who have access to its category. If not enabled, the product will be visible to all users regardless of category access.')
    allowed_user_ids = fields.Many2many(comodel_name='res.users', string='Allowed Users', compute='_compute_allowed_user_ids', store=True)

    @api.depends('categ_id', 'is_category_visibility', 'categ_id.allowed_user_ids')
    def _compute_allowed_user_ids(self):
        for product in self:
            if product.is_category_visibility:
                continue
            else:
                product.allowed_user_ids = product.categ_id.allowed_user_ids if product.categ_id else False