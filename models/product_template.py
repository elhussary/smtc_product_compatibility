from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    compatible_brand_ids = fields.Many2many("product.brand", string="Brand")

    compatible_connection_ids = fields.Many2many("product.connection", string="Connection")

    def _search_get_detail(self, website, order, options):
        result = super()._search_get_detail(website, order, options)
        brand_ids = options.get("brand_ids")
        connection_ids = options.get("connection_ids")
        if brand_ids:
            result["base_domain"].append([("compatible_brand_ids", "in", brand_ids)])
        if connection_ids:
            result["base_domain"].append([("compatible_connection_ids", "in", connection_ids)])
        return result

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1.0, uom_id=False, only_template=False):
        """Override to include default_code in combination info for dynamic Reference update."""
        res = super()._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            uom_id=uom_id,
            only_template=only_template,
        )
        if res.get("product_id"):
            product = self.env["product.product"].browse(res["product_id"])
            res["default_code"] = product.default_code or ""
        return res


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_brand_ref(self):
        """Find the brand reference by matching the variant's 'Brand' attribute
        value name to a product.brand record."""
        self.ensure_one()
        # Check variant attribute values first
        brand_ptav = self.product_template_attribute_value_ids.filtered(lambda v: v.attribute_id.name == "Brand")
        if brand_ptav:
            brand = self.env["product.brand"].search([("name", "=", brand_ptav[0].name)], limit=1)
            if brand and brand.reference:
                return brand.reference, brand.name
        return False, False


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_brand_info_from_line(self):
        """Get brand reference and name from sale order line attributes."""
        self.ensure_one()
        # Check no_variant attribute values (on the sale line)
        brand_ptav = self.product_no_variant_attribute_value_ids.filtered(lambda v: v.attribute_id.name == "Brand")
        # Fallback: check the product variant's own attribute values
        if not brand_ptav:
            brand_ptav = self.product_id.product_template_attribute_value_ids.filtered(lambda v: v.attribute_id.name == "Brand")
        if brand_ptav:
            brand = self.env["product.brand"].search([("name", "=", brand_ptav[0].name)], limit=1)
            if brand and brand.reference:
                return brand.reference, brand.name
        return False, False

    def _get_sale_order_line_multiline_description_sale(self):
        """Override to add brand reference as a separate line in the description."""
        name = super()._get_sale_order_line_multiline_description_sale()

        brand_ref, brand_name = self._get_brand_info_from_line()
        if brand_ref:
            parts = name.split("\n", 1)
            default_code = self.product_id.default_code
            if default_code:
                ref_line = "Ref: %s%s" % (brand_ref, default_code)
            else:
                ref_line = "Brand Ref: %s" % brand_ref
            if len(parts) > 1:
                name = "%s\n%s\n%s" % (parts[0], ref_line, parts[1])
            else:
                name = "%s\n%s" % (parts[0], ref_line)
        return name


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.depends("sale_line_id")
    def _compute_description_picking(self):
        super()._compute_description_picking()
        for move in self:
            if not move.sale_line_id or move.description_picking_manual:
                continue
            brand_ref, brand_name = move.sale_line_id._get_brand_info_from_line()
            if brand_ref:
                default_code = move.product_id.default_code
                if default_code:
                    ref_line = "Ref: %s%s" % (brand_ref, default_code)
                else:
                    ref_line = "Brand Ref: %s" % brand_ref
                move.description_picking = move.description_picking + "\n" + ref_line if move.description_picking else ref_line
