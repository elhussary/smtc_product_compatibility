/** @odoo-module **/

import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

/**
 * Updates the Reference cell in the Specifications table when the user
 * selects a different variant (e.g. GH1 → GH2).
 */
export class VariantReferenceUpdater extends Interaction {
  static selector = ".oe_website_sale";

  dynamicContent = {
    "input.product_id": { "t-on-change": this.onProductIdChange },
  };

  async onProductIdChange(ev) {
    const productId = parseInt(ev.target.value);
    if (!productId) return;

    const refCell = document.getElementById("spec_reference_value");
    if (!refCell) return;

    const brandRef = refCell.dataset.brandRef || "";

    try {
      const result = await rpc("/web/dataset/call_kw", {
        model: "product.product",
        method: "read",
        args: [[productId], ["default_code"]],
        kwargs: {},
      });

      if (result && result.length > 0) {
        const defaultCode = result[0].default_code || "";
        let refText = "";
        if (defaultCode && brandRef) {
          refText = brandRef + defaultCode;
        } else if (defaultCode) {
          refText = defaultCode;
        } else if (brandRef) {
          refText = brandRef;
        }
        refCell.textContent = refText;
      }
    } catch (e) {
      console.warn("Could not update reference:", e);
    }
  }
}

registry
  .category("public.interactions")
  .add(
    "smtc_product_compatibility.variant_reference_updater",
    VariantReferenceUpdater,
  );
