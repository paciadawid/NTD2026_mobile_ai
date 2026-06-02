from __future__ import annotations

from typing import TYPE_CHECKING

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.shop.product_detail_page import ProductDetailPage

# ── Resource IDs ──────────────────────────────────────────────────────────────
# Appium prepends appPackage automatically for AppiumBy.ID short IDs.
_ID_PRODUCT_LIST = "productRV"


class ProductListPage(BasePage):
    """Page Object for the MDA product catalog screen."""

    # ── Public actions ────────────────────────────────────────────────────────

    def open_product_by_name(self, name: str) -> ProductDetailPage:
        """Scroll to the product with the given title and open its detail page."""
        from pages.shop.product_detail_page import ProductDetailPage

        self._find(_ID_PRODUCT_LIST)

        # Scroll the matching title into the hierarchy, then tap its sibling image.
        # Two steps are needed because scrollIntoView ignores fromParent constraints
        # and always picks the first productIV it finds.
        self._driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().text("{name}"))',
        )
        self._driver.find_element(
            AppiumBy.XPATH,
            f'//android.widget.TextView[@text="{name}"]'
            f'/../android.widget.ImageView[contains(@resource-id,"productIV")]',
        ).click()

        return ProductDetailPage(self._driver)
