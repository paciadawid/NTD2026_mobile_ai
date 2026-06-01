import pytest


@pytest.mark.smoke
def test_two_plus_two_equals_four(calculator_page) -> None:
    calculator_page.clear().digit(2).add().digit(2).equals()
    assert calculator_page.result() == "4"
