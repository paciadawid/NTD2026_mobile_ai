import pytest

from pages.calculator_page import CalculatorPage


@pytest.mark.smoke
def test_two_plus_two_equals_four(driver) -> None:
    calc = CalculatorPage(driver)
    calc.clear().digit(2).add().digit(2).equals()
    assert calc.result() == "4"
