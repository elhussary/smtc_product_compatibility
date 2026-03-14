{
    "name": "SMTC Product Compatibility",
    "version": "1.0",
    "summary": "Manage Brands and Connections for Products",
    "category": "Sales",
    "depends": ["sale_management", "website_sale", "sale_stock", "website_sale_comparison"],
    "data": [
        "security/ir.model.access.csv",
        "views/compatibility_views.xml",
        "views/product_template_views.xml",
        "views/website_sale_templates.xml",
        "views/website_sale_filters.xml",
        "views/stock_picking_label.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "smtc_product_compatibility/static/src/css/style.css",
            "smtc_product_compatibility/static/src/js/compatibility_filter.js",
            "smtc_product_compatibility/static/src/js/variant_reference.js",
        ],
    },
    "installable": True,
    "application": False,
}
