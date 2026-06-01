from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

# ── Resource IDs ──────────────────────────────────────────────────────────────
_PKG = "com.google.android.calculator"

_ID_CLR = f"{_PKG}:id/clr"
_ID_DIGIT = f"{_PKG}:id/digit_"  # append digit 0-9
_ID_ADD = f"{_PKG}:id/op_add"
_ID_SUB = f"{_PKG}:id/op_sub"
_ID_MUL = f"{_PKG}:id/op_mul"
_ID_DIV = f"{_PKG}:id/op_div"
_ID_EQ = f"{_PKG}:id/eq"
_ID_RESULT = f"{_PKG}:id/result_final"

_TIMEOUT = 10  # seconds


class CalculatorPage:
    """Page Object for the Google Calculator app.

    All element look-ups use explicit waits so the page works reliably
    on both local emulators and real BrowserStack devices (which may be slower).
    """

    def __init__(self, driver) -> None:
        self._driver = driver
        self._wait = WebDriverWait(driver, _TIMEOUT)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _find(self, resource_id: str):
        return self._wait.until(ec.presence_of_element_located((AppiumBy.ID, resource_id)))

    def _tap(self, resource_id: str) -> CalculatorPage:
        self._find(resource_id).click()
        return self  # fluent API — allows chaining

    # ── Public actions ────────────────────────────────────────────────────────

    def clear(self) -> CalculatorPage:
        """Press AC / CLR to reset the calculator to a blank state."""
        return self._tap(_ID_CLR)

    def digit(self, n: int) -> CalculatorPage:
        """Press digit key 0-9."""
        if n not in range(10):
            raise ValueError(f"Digit must be 0-9, got {n}")
        return self._tap(f"{_ID_DIGIT}{n}")

    def add(self) -> CalculatorPage:
        return self._tap(_ID_ADD)

    def subtract(self) -> CalculatorPage:
        return self._tap(_ID_SUB)

    def multiply(self) -> CalculatorPage:
        return self._tap(_ID_MUL)

    def divide(self) -> CalculatorPage:
        return self._tap(_ID_DIV)

    def equals(self) -> CalculatorPage:
        return self._tap(_ID_EQ)

    # ── Assertions / queries ──────────────────────────────────────────────────

    def result(self) -> str:
        """Return the text shown in the result field."""
        return self._find(_ID_RESULT).text
