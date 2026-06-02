from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

_ACCEPT = 'new UiSelector().text("Yes, I agree")'


class PrivacyPage(BasePage):

    def accept(self) -> None:
        self._click(AppiumBy.ANDROID_UIAUTOMATOR, _ACCEPT)
