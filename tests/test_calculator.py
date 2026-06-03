import pytest
from appium import webdriver

from pages.calculator_page import CalculatorPage


@pytest.mark.smoke
def test_calculator_app_launches(driver: webdriver.Remote) -> None:
    """Smoke: verify the calculator app starts and the driver session is fully operational."""
    assert driver.session_id, "Session ID is empty — driver session was not created"
    assert driver.current_activity is not None, "No current activity — app may have failed to launch"
    assert any("NATIVE" in ctx for ctx in driver.contexts), (
        f"No native context found. Available contexts: {driver.contexts}"
    )


@pytest.mark.regression
def test_addition_one_plus_one_equals_two(calculator_page: CalculatorPage) -> None:
    """Verify that 1 + 1 = 2 in the Google Calculator."""
    calculator_page.press_digit(1)
    calculator_page.press_add()
    calculator_page.press_digit(1)
    calculator_page.press_equals()

    result = calculator_page.get_result()
    assert result == "2", f"Expected '2' but got '{result}'"


@pytest.mark.regression
def test_sin_of_90_degrees_equals_1(calculator_page: CalculatorPage) -> None:
    """Verify that sin(90) = 1 in the Google Calculator."""
    calculator_page.press_expand_scientific()
    calculator_page.press_sin()
    calculator_page.press_digit(9)
    calculator_page.press_digit(0)
    calculator_page.press_equals()

    result = calculator_page.get_result()
    assert result == "1", f"Expected '1' but got '{result}'"
