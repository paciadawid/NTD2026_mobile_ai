from __future__ import annotations

import re
from typing import TYPE_CHECKING

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.cart_page import CartPage

# ── Resource IDs ──────────────────────────────────────────────────────────────
# Appium prepends appPackage automatically for AppiumBy.ID short IDs.
_ID_PRICE = "priceTV"
_ID_MINUS = "minusIV"
_ID_PLUS = "plusIV"
_ID_QTY = "noTV"
_ID_ADD_TO_CART = "cartBt"
_ID_CART_NAV = "cartRL"


class ProductDetailPage(BasePage):
    """Page Object for the MDA product detail screen."""

    # ── Public actions ────────────────────────────────────────────────────────

    def price(self) -> str:
        """Return the unit price text, e.g. '$ 29.99'."""
        return self._text(_ID_PRICE)

    def price_as_float(self) -> float:
        """Return the unit price as a float, e.g. 29.99."""
        return float(re.sub(r"[^\d.]", "", self.price()))

    def set_quantity(self, quantity: int) -> ProductDetailPage:
        """Tap + or - until the quantity counter reaches *quantity*.

        Raises ValueError if the counter does not reach the target after all taps,
        which catches missed taps on slow devices.
        """
        current = int(self._text(_ID_QTY))
        for _ in range(quantity - current):
            self._tap(_ID_PLUS)
        for _ in range(current - quantity):
            self._tap(_ID_MINUS)
        actual = int(self._text(_ID_QTY))
        if actual != quantity:
            raise ValueError(f"set_quantity: expected {quantity}, got {actual}")
        return self

    def add_to_cart(self) -> ProductDetailPage:
        """Tap 'Add to cart'."""
        return self._tap(_ID_ADD_TO_CART)

    def go_to_cart(self) -> CartPage:
        """Tap the cart icon in the header and return the Cart page."""
        from pages.cart_page import CartPage

        self._tap(_ID_CART_NAV)
        return CartPage(self._driver)
