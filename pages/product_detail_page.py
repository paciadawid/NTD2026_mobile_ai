from __future__ import annotations

from typing import TYPE_CHECKING

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.product_list_page import ProductListPage


class ProductDetailPage(BasePage):
    """Page Object for the product detail screen (shopping app).

    Locators confirmed via get_page_source in Phase 1 MCP exploration.
    """

    # ── Locators ─────────────────────────────────────────────────────────────
    BTN_PLUS = (AppiumBy.ID, "plusIV")  # content-desc="Increase item quantity"
    BTN_MINUS = (AppiumBy.ID, "minusIV")  # content-desc="Decrease item quantity"
    TXT_QUANTITY = (AppiumBy.ID, "noTV")  # displays current qty, e.g. "1"
    BTN_ADD_TO_CART = (AppiumBy.ID, "cartBt")  # text="Add to cart"

    # ── Public actions ────────────────────────────────────────────────────────

    def set_quantity(self, quantity: int) -> None:
        """Set the item quantity by tapping + until the desired number is shown.

        Starts from whatever the current quantity is and only taps + (never -),
        so call this before adding to cart on a freshly opened detail page.
        """
        for _ in range(quantity - 1):
            self._tap(self.BTN_PLUS)

    def add_to_cart(self) -> ProductListPage:
        """Tap 'Add to cart' and return the ProductListPage (app stays on detail briefly)."""
        from pages.product_list_page import ProductListPage  # noqa: PLC0415

        self._tap(self.BTN_ADD_TO_CART)
        return ProductListPage(self.driver, self._wait._timeout)

    def back_to_product_list(self) -> ProductListPage:
        """Press the Android back button and return a ProductListPage."""
        from pages.product_list_page import ProductListPage  # noqa: PLC0415

        self._go_back()
        return ProductListPage(self.driver, self._wait._timeout)

    def get_quantity(self) -> str:
        """Return the current quantity text shown on screen."""
        return self._get_text(self.TXT_QUANTITY)
