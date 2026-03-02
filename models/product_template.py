from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    compatible_brand_ids = fields.Many2many("product.brand", string="Brands")

    compatible_connection_ids = fields.Many2many("product.connection", string="Connections")

    def _search_get_detail(self, website, order, options):
        result = super()._search_get_detail(website, order, options)
        brand_ids = options.get("brand_ids")
        connection_ids = options.get("connection_ids")
        if brand_ids:
            result["base_domain"].append([("compatible_brand_ids", "in", brand_ids)])
        if connection_ids:
            result["base_domain"].append([("compatible_connection_ids", "in", connection_ids)])
        return result
