"""E2E test: find the first available one-way flight from Tallinn (TLL) to Dublin (DUB)."""


def test_first_available_flight_tll_to_dub(
    privacy_page,
    login_page,
    home_page,
    find_flights_page,
    airport_picker_page,
    date_picker_page,
    results_page,
):
    privacy_page.accept()
    login_page.continue_as_guest()

    home_page.dismiss_promo_popup()
    home_page.tap_book_a_flight()

    find_flights_page.allow_location_if_asked()
    find_flights_page.select_one_way()

    find_flights_page.tap_origin_field()
    airport_picker_page.search_and_select("Tallinn")

    find_flights_page.tap_destination_field()
    airport_picker_page.select("Dublin")

    find_flights_page.tap_date_field()
    date_picker_page.select_first_available()

    find_flights_page.search()
    results_page.wait_for_results()

    assert results_page.departure_airport == "TLL"
    assert results_page.arrival_airport == "DUB"
    assert results_page.flight_number.startswith("FR")
    assert results_page.price > 0
