from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

LOCATION_ALLOW = "com.android.permissioncontroller:id/permission_allow_foreground_only_button"

# The Find Flights form fields are Compose android.view.View containers.
# Their @text attribute is unreliable (sometimes empty, sometimes aggregated from children).
# Target them by matching a child TextView label instead — robust across all render states.
# "One way" / "Return" / "Multicity" are native TextViews — UIAutomator works fine there.
_ONE_WAY    = 'new UiSelector().text("One way")'
_FROM       = '//android.view.View[@clickable="true" and .//android.widget.TextView[@text="From"]]'
_TO         = '//android.view.View[@clickable="true" and .//android.widget.TextView[@text="To"]]'
_DATES      = '//android.view.View[@clickable="true" and .//android.widget.TextView[contains(@text,"Date")]]'
_LETS_GO    = '//android.view.View[@clickable="true" and .//android.widget.TextView[contains(@text,"go")]]'
_PROMO_CLOSE = 'new UiSelector().className("android.widget.Button").instance(0)'

_UIA   = AppiumBy.ANDROID_UIAUTOMATOR
_XPATH = AppiumBy.XPATH


class FindFlightsPage(BasePage):

    def allow_location_if_asked(self) -> None:
        """Grant location access and dismiss any promo popup that may appear."""
        self._try_click(AppiumBy.ID, LOCATION_ALLOW)
        self._try_click(_UIA, _PROMO_CLOSE)

    def select_one_way(self) -> None:
        self._click(_UIA, _ONE_WAY)
        # Wait for the Compose form to finish re-rendering after the tab switch.
        # The "Date" field (singular, only present in one-way mode) becoming clickable
        # is the reliable signal that the transition animation is complete.
        self._wait_present(_XPATH, _DATES)

    def tap_origin_field(self) -> None:
        self._try_click(_UIA, _PROMO_CLOSE)  # promo may reappear after trip-type change
        self._click(_XPATH, _FROM)

    def tap_destination_field(self) -> None:
        self._try_click(_UIA, _PROMO_CLOSE)
        self._click(_XPATH, _TO)

    def tap_date_field(self) -> None:
        self._click(_XPATH, _DATES)

    def search(self) -> None:
        self._click(_XPATH, _LETS_GO)
