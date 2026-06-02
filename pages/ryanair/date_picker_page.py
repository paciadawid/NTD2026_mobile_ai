from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

_XPATH = AppiumBy.XPATH

# Date cells have content-desc like "Friday 2026-06-05".
# In Compose they are clickable=false but enabled=true in the a11y tree — drop the clickable filter.
# Element [1] is a large row-container for the first week; [2]=today, [5]=3 days out (first available).
# XPath is used because UIAutomator descriptionContains() does not match Compose content-desc.
_FIRST_AVAILABLE = '(//android.view.View[contains(@content-desc,"2026") and @enabled="true"])[5]'
# The "Select" button is a Compose Button with empty text (clickable=false, enabled=true).
# Use XPath targeting the single enabled Button on the date-picker screen.
_SELECT_BTN = '//android.widget.Button[@enabled="true"]'


class DatePickerPage(BasePage):

    def select_first_available(self) -> None:
        """Tap the first available date cell, then confirm with the Select button."""
        self._click(_XPATH, _FIRST_AVAILABLE)
        self._click(_XPATH, _SELECT_BTN)
