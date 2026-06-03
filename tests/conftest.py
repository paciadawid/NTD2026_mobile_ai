import pytest
from appium import webdriver

from pages.calculator_page import CalculatorPage
from pages.product_list_page import ProductListPage


@pytest.fixture()
def calculator_page(driver: webdriver.Remote) -> CalculatorPage:
    """Return a CalculatorPage bound to the current driver session."""
    return CalculatorPage(driver)


@pytest.fixture()
def product_list_page(driver: webdriver.Remote) -> ProductListPage:
    """Return a ProductListPage bound to the current driver session."""
    return ProductListPage(driver)
