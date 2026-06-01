"""
Smoke tests for Sauce Labs My Demo App — shopping flow.

Run locally:     uv run pytest tests/test_shop.py -v
Run on BS:       BS_TARGET=1 uv run pytest tests/test_shop.py -v
"""

import pytest

# ── Product name constants ────────────────────────────────────────────────────
YELLOW_BACKPACK = "Sauce Labs Backpack (yellow)"


@pytest.mark.smoke
def test_yellow_backpack_qty2_correct_total(product_list_page):
    """Add 2 units of the yellow backpack to the cart and verify the total price."""
    detail = product_list_page.open_product_by_name(YELLOW_BACKPACK)
    unit_price = detail.price_as_float()

    detail.set_quantity(2).add_to_cart()

    cart = detail.go_to_cart()
    assert cart.item_count() == "2 Items"
    assert cart.total_price_as_float() == pytest.approx(unit_price * 2, abs=0.01)
