from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

# The location permission dialog may appear the first time the picker loads.
# Do NOT add a generic className("Button").instance(0) here – it can match the picker's
# own back/close button and accidentally navigate away from the screen.
_LOCATION_ALLOW = "com.android.permissioncontroller:id/permission_allow_foreground_only_button"
_SEARCH_BOX     = 'new UiSelector().className("android.widget.EditText")'

_UIA = AppiumBy.ANDROID_UIAUTOMATOR


class AirportPickerPage(BasePage):

    def search_and_select(self, city: str) -> None:
        """Type *city* in the search box and tap the first matching result."""
        # Only dismiss the location permission dialog here; promo is handled before the picker opens.
        self._try_click(AppiumBy.ID, _LOCATION_ALLOW)
        self._type(_UIA, _SEARCH_BOX, city)
        # Use TextView to avoid matching the EditText that now also contains the typed text
        self._click(_UIA, f'new UiSelector().className("android.widget.TextView").text("{city}")')

    def select(self, city: str) -> None:
        """Tap *city* directly from the pre-populated list (no search needed)."""
        self._click(_UIA, f'new UiSelector().text("{city}")')
