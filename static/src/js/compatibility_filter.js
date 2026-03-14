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

  onFilterChange(ev) {
    const changedElement = ev.target;

    const productGrid = this.el.querySelector(
      ".o_wsale_products_grid_table_wrapper",
    );
    if (productGrid) {
      productGrid.classList.add("opacity-50");
    }

    const url = new URL(window.location.href);

    url.searchParams.delete("brand_id");
    url.searchParams.delete("connection_id");

    const brandSelect = this.el.querySelector('select[name="brand_id"]');
    const connSelect = this.el.querySelector('select[name="connection_id"]');

    if (brandSelect && brandSelect.value) {
      url.searchParams.set("brand_id", brandSelect.value);

      if (changedElement.name === "brand_id") {
        url.searchParams.delete("connection_id");
      } else if (connSelect && connSelect.value) {
        url.searchParams.set("connection_id", connSelect.value);
      }
    }

    window.location = `${url.pathname}${url.search}${url.hash}`;
  }
}

registry
  .category("public.interactions")
  .add("smtc_product_compatibility.compatibility_filter", CompatibilityFilter);
