import pytest

from pages.cart_page import CartPage
from pages.product_list_page import ProductListPage

_UNIT_PRICE = 29.99
_QUANTITY = 2
_EXPECTED_TOTAL_QTY2 = f"$ {_UNIT_PRICE * _QUANTITY:.2f}"
_EXPECTED_TOTAL_QTY1 = f"$ {_UNIT_PRICE:.2f}"


@pytest.mark.regression
def test_add_yellow_backpack_qty_2_validates_total_price(
    product_list_page: ProductListPage,
) -> None:
    """Add 2× yellow backpack to cart and verify the cart total equals $59.98."""
    product_detail = product_list_page.open_product("Sauce Labs Backpack (yellow)")

    product_detail.set_quantity(_QUANTITY)
    assert product_detail.get_quantity() == str(_QUANTITY), f"Expected quantity {_QUANTITY} on detail page"

    product_detail.add_to_cart()
    cart: CartPage = product_list_page.navigate_to_cart()

    total = cart.get_total_price()
    assert total == _EXPECTED_TOTAL_QTY2, f"Expected cart total '{_EXPECTED_TOTAL_QTY2}' but got '{total}'"


@pytest.mark.regression
def test_add_two_backpacks_remove_yellow_validates_violet_total(
    product_list_page: ProductListPage,
) -> None:
    """Add yellow + violet backpacks, remove yellow, verify only violet remains at correct price."""
    detail_yellow = product_list_page.open_product("Sauce Labs Backpack (yellow)")
    detail_yellow.add_to_cart()
    detail_yellow.back_to_product_list()

    detail_violet = product_list_page.open_product("Sauce Labs Backpack (violet)")
    detail_violet.add_to_cart()

    cart: CartPage = product_list_page.navigate_to_cart()
    cart.remove_item("yellow")

    item_names = cart.get_item_names()
    assert any("violet" in n for n in item_names), f"Violet backpack not found in cart: {item_names}"
    assert not any("yellow" in n for n in item_names), f"Yellow backpack still in cart: {item_names}"
    assert cart.get_items_count() == "1 Items", f"Expected '1 Items' but got '{cart.get_items_count()}'"
    assert cart.get_total_price() == _EXPECTED_TOTAL_QTY1, (
        f"Expected cart total '{_EXPECTED_TOTAL_QTY1}' but got '{cart.get_total_price()}'"
    )
