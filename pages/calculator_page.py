from __future__ import annotations

from pages.base_page import BasePage

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


class CalculatorPage(BasePage):
    """Page Object for the Google Calculator app.

    All element look-ups use explicit waits so the page works reliably
    on both local emulators and real BrowserStack devices (which may be slower).
    """

    # ── Public actions ────────────────────────────────────────────────────────

    def clear(self) -> CalculatorPage:
        """Press AC / CLR to reset the calculator to a blank state."""
        return self._tap(_ID_CLR)

    def digit(self, n: int) -> CalculatorPage:
        """Press digit key 0-9."""
        if n not in range(10):
            raise ValueError(f"Digit must be 0-9, got {n}")
        return self._tap(f"{_ID_DIGIT}{n}")

    def number(self, n: int) -> CalculatorPage:
        """Enter a non-negative integer by pressing its digits in sequence."""
        if n < 0:
            raise ValueError(f"Use subtract() before number() for negatives, got {n}")
        for ch in str(n):
            self.digit(int(ch))
        return self

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
        return self._text(_ID_RESULT)
