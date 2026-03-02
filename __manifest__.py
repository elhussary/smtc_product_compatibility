{
    "name": "SMTC Product Compatibility",
    "version": "1.0",
    "summary": "Manage Brands and Connections for Products",
    "category": "Sales",
    "depends": ["sale_management", "website_sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/compatibility_views.xml",
        "views/product_template_views.xml",
        "views/website_sale_templates.xml",
        "views/website_sale_filters.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "smtc_product_compatibility/static/src/js/compatibility_filter.js",
        ],
    },
    "installable": True,
    "application": False,
}
