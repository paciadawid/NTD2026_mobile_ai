import pytest
from appium import webdriver

from pages.calculator_page import CalculatorPage


@pytest.fixture()
def calculator_page(driver: webdriver.Remote) -> CalculatorPage:
    """Return a CalculatorPage bound to the current driver session."""
    return CalculatorPage(driver)
