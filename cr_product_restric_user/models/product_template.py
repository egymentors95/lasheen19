# -*- coding: utf-8 -*-
# Part of Creyox Technologies
from odoo import models, api
from odoo.osv.expression import AND


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _search(
        self,
        domain,
        offset=0,
        limit=None,
        order=None,
        count=False,
        bypass_access=False,
    ):
        user = self.env.user
        restricted_group = self.env.ref(
            "cr_product_restric_user.cr_product_restriction_on_user",
            raise_if_not_found=False,
        )

        if restricted_group and restricted_group in user.group_ids:
            if user.cr_restriction_on == "product":
                ids = user.cr_product_template_ids.ids
                if ids:
                    domain = AND([domain, [("id", "in", ids)]])
                else:
                    return 0 if count else []

            elif user.cr_restriction_on == "category":
                ids = user.cr_product_category_ids.ids
                if ids:
                    domain = AND([domain, [("categ_id", "in", ids)]])
                else:
                    return 0 if count else []

        return super()._search(
            domain,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            bypass_access=bypass_access,
        )


class Product(models.Model):
    _inherit = "product.product"

    @api.model
    def _search(
        self,
        domain,
        offset=0,
        limit=None,
        order=None,
        count=False,
        bypass_access=False,
    ):
        user = self.env.user
        restricted_group = self.env.ref(
            "cr_product_restric_user.cr_product_restriction_on_user",
            raise_if_not_found=False,
        )

        if restricted_group and restricted_group in user.group_ids:
            if user.cr_restriction_on == "product":
                ids = user.cr_product_template_ids.ids
                if ids:
                    domain = AND([domain, [("product_tmpl_id", "in", ids)]])
                else:
                    return 0 if count else []

            elif user.cr_restriction_on == "category":
                ids = user.cr_product_category_ids.ids
                if ids:
                    domain = AND([domain, [("categ_id", "in", ids)]])
                else:
                    return 0 if count else []

        return super()._search(
            domain,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            bypass_access=bypass_access,
        )