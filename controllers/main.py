from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCompatibility(WebsiteSale):

    def _get_selected_brand_connection(self):
        """Read brand/connection filter IDs from URL params."""
        brand_ids = [int(b) for b in request.httprequest.args.getlist("brand_id")]

        # IF NO BRAND IS SELECTED, SELECT THE FIRST BRAND
        if not brand_ids:
            first_brand = request.env["product.brand"].search([], limit=1)
            if first_brand:
                brand_ids = [first_brand.id]

        connection_ids = [int(c) for c in request.httprequest.args.getlist("connection_id")]
        brands = request.env["product.brand"].browse(brand_ids).exists()

        # If brand is selected but no connection, select first available connection
        if brands and not connection_ids:
            first_connection = request.env["product.connection"].search([("brand_id", "in", brands.ids)], limit=1)
            if first_connection:
                connection_ids = [first_connection.id]

        connections = request.env["product.connection"].browse(connection_ids).exists()
        return brand_ids, connection_ids, brands, connections

    @http.route()
    def shop(self, page=0, category=None, search="", min_price=0.0, max_price=0.0, tags="", **post):
        response = super().shop(
            page=page,
            category=category,
            search=search,
            min_price=min_price,
            max_price=max_price,
            tags=tags,
            **post,
        )
        all_brands = request.env["product.brand"].search([])
        all_connections = request.env["product.connection"].search([])
        brand_ids, connection_ids, sel_brands, sel_connections = self._get_selected_brand_connection()
        # Store in session so product detail page can access them
        request.session["compat_brand_ids"] = brand_ids
        request.session["compat_connection_ids"] = connection_ids
        response.qcontext.update(
            {
                "all_brands": all_brands,
                "all_connections": all_connections,
                "selected_brand_ids": brand_ids,
                "selected_connection_ids": connection_ids,
                "selected_brands": sel_brands,
                "selected_connections": sel_connections,
            }
        )

        return response

    def _prepare_product_values(self, product, category, **kwargs):
        # Get the selected brand/connection from URL params or session
        brand_ids = [int(b) for b in request.httprequest.args.getlist("brand_id")]
        connection_ids = [int(c) for c in request.httprequest.args.getlist("connection_id")]
        if not brand_ids:
            brand_ids = request.session.get("compat_brand_ids", [])
        if not connection_ids:
            connection_ids = request.session.get("compat_connection_ids", [])
        sel_brands = request.env["product.brand"].browse(brand_ids).exists()
        sel_connections = request.env["product.connection"].browse(connection_ids).exists()
        # Find matching product.attribute.value IDs to pre-select variant combination
        if not kwargs.get("attribute_values") and (sel_brands or sel_connections):
            attr_value_ids = []
            for brand in sel_brands[:1]:
                # Find attribute value in "Brand" attribute that matches this brand name
                pav = request.env["product.attribute.value"].search(
                    [
                        ("name", "=", brand.name),
                        ("attribute_id.name", "=", "Brand"),
                    ],
                    limit=1,
                )

                if pav:
                    attr_value_ids.append(pav.id)
            for conn in sel_connections[:1]:
                # Find attribute value in "Connection" attribute that matches this connection name
                pav = request.env["product.attribute.value"].search(
                    [
                        ("name", "=", conn.name),
                        ("attribute_id.name", "=", "Connection"),
                    ],
                    limit=1,
                )

                if pav:
                    attr_value_ids.append(pav.id)
            if attr_value_ids:
                kwargs["attribute_values"] = ",".join(str(v) for v in attr_value_ids)
        values = super()._prepare_product_values(product, category, **kwargs)
        values.update(
            {
                "selected_brand_ids": brand_ids,
                "selected_connection_ids": connection_ids,
                "selected_brands": sel_brands,
                "selected_connections": sel_connections,
            }
        )

        return values

    def _get_search_options(self, **post):
        options = super()._get_search_options(**post)
        options["brand_ids"] = [int(b) for b in request.httprequest.args.getlist("brand_id")]
        options["connection_ids"] = [int(c) for c in request.httprequest.args.getlist("connection_id")]
        return options

    def _shop_get_query_url_kwargs(self, search, min_price, max_price, **kwargs):
        """Ensure brand/connection params are preserved in QueryURL so that

        standard attribute filter changes preserve them."""
        result = super()._shop_get_query_url_kwargs(search, min_price, max_price, **kwargs)
        brand_ids = request.httprequest.args.getlist("brand_id")
        connection_ids = request.httprequest.args.getlist("connection_id")

        if brand_ids:
            result["brand_id"] = brand_ids

        if connection_ids:
            result["connection_id"] = connection_ids

        return result
