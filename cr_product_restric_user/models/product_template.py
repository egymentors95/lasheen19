# -*- coding: utf-8 -*-
# Part of Creyox Technologies
from odoo import models, api
from odoo.osv.expression import AND


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None):
        """Overriding the _search method to modify how products are searched"""
        user = self.env.user
        restricted_group = self.env.ref(
            "cr_product_restric_user.cr_product_restriction_on_user"
        )

        args = list(args or [])

        if restricted_group in user.group_ids:
            if user.cr_restriction_on == "product":
                product_ids = user.cr_product_template_ids.ids
                if product_ids:
                    args = AND([args, [("id", "in", product_ids)]])
                else:
                    return []

            elif user.cr_restriction_on == "category":
                category_ids = user.cr_product_category_ids.ids
                if category_ids:
                    args = AND([args, [("categ_id", "in", category_ids)]])
                else:
                    return []

        return super()._search(args, offset=offset, limit=limit, order=order)


class Product(models.Model):
    _inherit = "product.product"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None):
        """Overriding the _search method to modify how products are searched"""
        user = self.env.user
        restricted_group = self.env.ref(
            "cr_product_restric_user.cr_product_restriction_on_user"
        )

        args = list(args or [])

        if restricted_group in user.group_ids:
            if user.cr_restriction_on == "product":
                template_ids = user.cr_product_template_ids.ids
                if template_ids:
                    args = AND([args, [("product_tmpl_id", "in", template_ids)]])
                else:
                    return []

            elif user.cr_restriction_on == "category":
                category_ids = user.cr_product_category_ids.ids
                if category_ids:
                    args = AND([args, [("categ_id", "in", category_ids)]])
                else:
                    return []

        return super()._search(args, offset=offset, limit=limit, order=order)
