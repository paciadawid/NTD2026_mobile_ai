import os

from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

_DEFAULT_WAIT_TIMEOUT = int(os.getenv("WAIT_TIMEOUT", "10"))


class BasePage:
    """Shared base for all Page Objects.

    Provides the driver/wait wiring and the small set of primitive interactions
    (_tap, _get_text) so concrete pages never repeat boilerplate.
    """

    def __init__(self, driver: webdriver.Remote, timeout: int = _DEFAULT_WAIT_TIMEOUT) -> None:
        self.driver = driver
        self._wait = WebDriverWait(driver, timeout)

    def _tap(self, locator: tuple[str, str]) -> None:
        """Wait for *locator* to be clickable, then tap it."""
        self._wait.until(EC.element_to_be_clickable(locator)).click()

    def _get_text(self, locator: tuple[str, str]) -> str:
        """Wait for *locator* to be visible and return its text."""
        return self._wait.until(EC.visibility_of_element_located(locator)).text

    def _go_back(self) -> None:
        """Press the Android back button."""
        self.driver.back()
