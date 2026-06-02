from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

_CONTINUE_AS_GUEST = 'new UiSelector().text("Continue as guest")'


class LoginPage(BasePage):

    def continue_as_guest(self) -> None:
        self._click(AppiumBy.ANDROID_UIAUTOMATOR, _CONTINUE_AS_GUEST)
