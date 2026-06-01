from __future__ import annotations

from typing import Self

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

TIMEOUT = 15  # seconds


class BasePage:
    def __init__(self, driver: webdriver.Remote) -> None:
        self._driver = driver
        self._wait = WebDriverWait(driver, TIMEOUT)

    def _find(self, resource_id: str):
        """Wait until the element is visible and return it."""
        return self._wait.until(ec.visibility_of_element_located((AppiumBy.ID, resource_id)))

    def _tap(self, resource_id: str) -> Self:
        """Wait until the element is clickable, tap it, and return self for chaining."""
        self._wait.until(ec.element_to_be_clickable((AppiumBy.ID, resource_id))).click()
        return self

    def _text(self, resource_id: str) -> str:
        """Find an element and read its text atomically, retrying on staleness.

        Wraps the result in a tuple so that elements with empty-string text don't
        look falsy and cause the wait to keep retrying indefinitely.
        Catches StaleElementReferenceException so a mid-read re-render causes a
        retry rather than a crash.
        """
        def _read(d) -> tuple[str] | bool:
            try:
                el = d.find_element(AppiumBy.ID, resource_id)
                return (el.text,) if el.text is not None else False
            except StaleElementReferenceException:
                return False

        return self._wait.until(_read)[0]
