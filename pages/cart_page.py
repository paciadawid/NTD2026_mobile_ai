from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

# Full resource-id prefix used in all cart locators
_PKG = "com.saucelabs.mydemoapp.android:id"


class CartPage(BasePage):
    """Page Object for the cart / basket screen (shopping app).

    Locators confirmed via get_page_source in Phase 1 MCP exploration.
    """

    # ── Locators ─────────────────────────────────────────────────────────────
    TXT_TOTAL_PRICE = (AppiumBy.ID, "totalPriceTV")  # e.g. "$ 59.98"
    TXT_ITEMS_COUNT = (AppiumBy.ID, "itemsTV")  # e.g. "2 Items"

    # ── Public accessors ──────────────────────────────────────────────────────

    def get_total_price(self) -> str:
        """Return the total price string shown at the bottom of the cart, e.g. '$ 59.98'."""
        return self._get_text(self.TXT_TOTAL_PRICE)

    def get_items_count(self) -> str:
        """Return the items-count label shown next to the total, e.g. '2 Items'."""
        return self._get_text(self.TXT_ITEMS_COUNT)

    def get_item_names(self) -> list[str]:
        """Return a list of all product title strings currently visible in the cart."""
        elements = self._wait.until(EC.presence_of_all_elements_located((AppiumBy.ID, f"{_PKG}/titleTV")))
        return [el.text for el in elements if el.text]

    def remove_item(self, name_contains: str) -> None:
        """Tap 'Remove Item' for the cart row whose title contains *name_contains*.

        Locator confirmed via get_page_source in Phase 1 MCP exploration:
          removeBt  content-desc="Removes product from cart"
        XPath navigates from the matching titleTV up two ancestors then down to removeBt.
        """
        locator = (
            AppiumBy.XPATH,
            f'//android.widget.TextView[@resource-id="{_PKG}/titleTV"'
            f' and contains(@text,"{name_contains}")]'
            f'/../..//android.widget.TextView[@resource-id="{_PKG}/removeBt"]',
        )
        self._tap(locator)
