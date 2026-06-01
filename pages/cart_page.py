from __future__ import annotations

import re

from pages.base_page import BasePage

# ── Resource IDs ──────────────────────────────────────────────────────────────
# Appium prepends appPackage automatically for AppiumBy.ID short IDs.
_ID_ITEMS_COUNT = "itemsTV"
_ID_TOTAL_PRICE = "totalPriceTV"


class CartPage(BasePage):
    """Page Object for the MDA cart / basket screen."""

    # ── Assertions / queries ──────────────────────────────────────────────────

    def item_count(self) -> str:
        """Return the item-count summary text, e.g. '2 Items'."""
        return self._text(_ID_ITEMS_COUNT)

    def total_price(self) -> str:
        """Return the total price text, e.g. '$ 59.98'."""
        return self._text(_ID_TOTAL_PRICE)

    def total_price_as_float(self) -> float:
        """Return the total price as a float, e.g. 59.98."""
        return float(re.sub(r"[^\d.]", "", self.total_price()))
