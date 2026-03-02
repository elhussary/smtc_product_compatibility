from odoo import models, fields


class ProductBrand(models.Model):
    _name = "product.brand"
    _description = "Product Brand"

    name = fields.Char(string="Brand Name", required=True)


class ProductConnection(models.Model):
    _name = "product.connection"
    _description = "Product Connection"

    name = fields.Char(string="Connection Name", required=True)
    brand_id = fields.Many2one("product.brand", string="Brand", required=True)
