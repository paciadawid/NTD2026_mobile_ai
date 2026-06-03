from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class CalculatorPage(BasePage):
    """Page Object for the Google Calculator main screen."""

    # --- display ---
    FORMULA = (AppiumBy.ID, "formula")
    RESULT_FINAL = (AppiumBy.ID, "result_final")
    RESULT_PREVIEW = (AppiumBy.ID, "result_preview")

    # --- scientific panel ---
    BTN_EXPAND_SCIENTIFIC = (AppiumBy.ID, "collapse_expand")
    BTN_SIN = (AppiumBy.ID, "fun_sin")

    # --- operators ---
    BTN_ADD = (AppiumBy.ID, "op_add")
    BTN_SUB = (AppiumBy.ID, "op_sub")
    BTN_MUL = (AppiumBy.ID, "op_mul")
    BTN_DIV = (AppiumBy.ID, "op_div")
    BTN_EQUALS = (AppiumBy.ID, "eq")
    BTN_CLEAR = (AppiumBy.ID, "clr")

    # --- digits (looked up dynamically via _DIGIT_IDS) ---
    _DIGIT_IDS: dict[int, tuple[str, str]] = {i: (AppiumBy.ID, f"digit_{i}") for i in range(10)}

    def press_digit(self, digit: int) -> None:
        """Tap a digit button (0–9)."""
        self._tap(self._DIGIT_IDS[digit])

    def press_add(self) -> None:
        self._tap(self.BTN_ADD)

    def press_equals(self) -> None:
        self._tap(self.BTN_EQUALS)

    def press_expand_scientific(self) -> None:
        """Tap the expand button to reveal the scientific keypad."""
        self._tap(self.BTN_EXPAND_SCIENTIFIC)

    def press_sin(self) -> None:
        """Tap the sin function button (scientific panel must be expanded first)."""
        self._tap(self.BTN_SIN)

    def press_clear(self) -> None:
        self._tap(self.BTN_CLEAR)

    def get_result(self) -> str:
        """Return the final result shown after pressing equals (result_final field)."""
        return self._get_text(self.RESULT_FINAL)

    def get_result_preview(self) -> str:
        """Return the live result preview shown while entering a formula."""
        return self._get_text(self.RESULT_PREVIEW)
