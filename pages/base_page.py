from __future__ import annotations

from typing import Self

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

TIMEOUT = 15       # seconds — used for required elements
SHORT_TIMEOUT = 5  # seconds — used for optional/conditional elements


class BasePage:
    def __init__(self, driver: webdriver.Remote) -> None:
        self._driver = driver
        self._wait = WebDriverWait(driver, TIMEOUT, ignored_exceptions=[StaleElementReferenceException])
        self._wait_short = WebDriverWait(driver, SHORT_TIMEOUT, ignored_exceptions=[StaleElementReferenceException])

    # ── Generic interaction helpers ───────────────────────────────────────────

    def _click(self, by: str, locator: str) -> None:
        """Wait until element is clickable and click it."""
        self._wait.until(ec.element_to_be_clickable((by, locator))).click()

    def _type(self, by: str, locator: str, text: str) -> None:
        """Wait until element is clickable and type *text* into it."""
        self._wait.until(ec.element_to_be_clickable((by, locator))).send_keys(text)

    def _try_click(self, by: str, locator: str) -> None:
        """Click element if it appears within the short timeout; silently skip if absent."""
        try:
            self._wait_short.until(ec.element_to_be_clickable((by, locator))).click()
        except Exception:
            pass

    def _wait_present(self, by: str, locator: str, timeout: int | None = None) -> None:
        """Block until the element is present in the DOM.

        Uses *timeout* seconds when supplied, otherwise falls back to ``self._wait``.
        """
        wait = WebDriverWait(self._driver, timeout) if timeout is not None else self._wait
        wait.until(ec.presence_of_element_located((by, locator)))

    # ── ID-based convenience shortcuts ────────────────────────────────────────

    def _find(self, resource_id: str):
        """Wait until the element is visible and return it (by resource-id)."""
        return self._wait.until(ec.visibility_of_element_located((AppiumBy.ID, resource_id)))

    def _tap(self, resource_id: str) -> Self:
        """Shorthand for ``_click(AppiumBy.ID, resource_id)``; returns self for chaining."""
        self._click(AppiumBy.ID, resource_id)
        return self

    def _text(self, resource_id: str) -> str:
        """Read element text atomically by resource-id, retrying on staleness."""
        def _read(d) -> tuple[str] | bool:
            try:
                el = d.find_element(AppiumBy.ID, resource_id)
                return (el.text,) if el.text is not None else False
            except StaleElementReferenceException:
                return False

        return self._wait.until(_read)[0]
