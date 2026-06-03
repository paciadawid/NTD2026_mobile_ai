from __future__ import annotations

from typing import TYPE_CHECKING

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.cart_page import CartPage
    from pages.product_detail_page import ProductDetailPage


class ProductListPage(BasePage):
    """Page Object for the product catalogue screen (shopping app).

    Locators confirmed via get_page_source in Phase 1 MCP exploration.
    """

    # ── Locators ─────────────────────────────────────────────────────────────
    # resource-id short forms — package prefix resolved automatically by UiAutomator2
    PRODUCT_RV = (AppiumBy.ID, "productRV")

    # ── Private helpers ───────────────────────────────────────────────────────

    def _scroll_to_product(self, name_contains: str) -> None:
        """Scroll the product list until a product whose title contains *name_contains* is visible."""
        self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f"new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView("
            f'new UiSelector().textContains("{name_contains}"))',
        )

    # ── Public actions ────────────────────────────────────────────────────────

    def navigate_to_cart(self) -> CartPage:
        """Tap the cart icon in the app header and return the CartPage.

        Locator confirmed via get_page_source in Phase 1 MCP exploration:
          content-desc="View cart"  resource-id="cartRL"
        """
        from pages.cart_page import CartPage  # noqa: PLC0415 — deferred to avoid circular import

        self._tap((AppiumBy.ACCESSIBILITY_ID, "View cart"))
        return CartPage(self.driver, self._wait._timeout)

    def open_product(self, name_contains: str) -> ProductDetailPage:
        """Scroll to the product whose title contains *name_contains* and tap its image.

        Returns the ProductDetailPage for the opened product.
        """
        from pages.product_detail_page import ProductDetailPage  # noqa: PLC0415

        self._scroll_to_product(name_contains)
        # Tap the clickable image that sits as a preceding sibling of the title TextView.
        # Structure confirmed in MCP Phase 1:
        #   <ViewGroup>
        #     <ImageView content-desc="Product Image" clickable="true" />   ← tap this
        #     <TextView  content-desc="Product Title" text="… (yellow)" />
        #   </ViewGroup>
        image_locator = (
            AppiumBy.XPATH,
            f'//android.widget.TextView[@text="{name_contains}"]'
            f'/preceding-sibling::android.widget.ImageView[@content-desc="Product Image"]',
        )
        self._tap(image_locator)
        return ProductDetailPage(self.driver, self._wait._timeout)
