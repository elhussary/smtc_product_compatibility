/** @odoo-module **/

import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";

export class CompatibilityFilter extends Interaction {
    static selector = ".oe_website_sale";

    dynamicContent = {
        ".compatibility_filter": {
            "t-on-change": this.onFilterChange,
        },
    };

    onFilterChange() {
        // Show loading effect on the product grid
        const productGrid = this.el.querySelector(".o_wsale_products_grid_table_wrapper");
        if (productGrid) {
            productGrid.classList.add("opacity-50");
        }

        // Build URL from the current page URL
        const url = new URL(window.location.href);

        // Remove old brand/connection params
        url.searchParams.delete("brand_id");
        url.searchParams.delete("connection_id");

        // Read selected brand from dropdown
        const brandSelect = this.el.querySelector('select[name="brand_id"]');
        if (brandSelect && brandSelect.value) {
            url.searchParams.set("brand_id", brandSelect.value);
        }

        // Read selected connection from dropdown
        const connSelect = this.el.querySelector('select[name="connection_id"]');
        if (connSelect && connSelect.value) {
            url.searchParams.set("connection_id", connSelect.value);
        }

        window.location = `${url.pathname}?${url.searchParams.toString()}`;
    }
}

registry
    .category("public.interactions")
    .add("smtc_product_compatibility.compatibility_filter", CompatibilityFilter);
