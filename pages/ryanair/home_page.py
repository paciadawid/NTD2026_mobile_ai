from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

BOOK_A_FLIGHT = "container_search"
_PROMO_CLOSE  = 'new UiSelector().className("android.widget.Button").instance(0)'


class HomePage(BasePage):

    def dismiss_promo_popup(self) -> None:
        """Close the promotional overlay if it appears after login."""
        self._try_click(AppiumBy.ANDROID_UIAUTOMATOR, _PROMO_CLOSE)

    def tap_book_a_flight(self) -> None:
        self._tap(BOOK_A_FLIGHT)
