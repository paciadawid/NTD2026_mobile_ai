"""Page object for the Ryanair flight results screen."""
from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

DEPARTURE_AIRPORT = "departure_airport"
ARRIVAL_AIRPORT   = "arrival_airport"
DEPARTURE_TIME    = "departure_time"
ARRIVAL_TIME      = "arrival_time"
FLIGHT_TIME       = "flight_time"
FLIGHT_NUMBER     = "flight_number"
PRICE             = "price"
CURRENCY          = "currency"
FLIGHTS_LEFT      = "flights_left"


class RyanairResultsPage(BasePage):
    """Provides accessors for flight data displayed on the search results screen."""

    def wait_for_results(self, timeout: int = 25) -> RyanairResultsPage:
        """Block until the departure airport code is visible (results have loaded)."""
        self._wait_present(AppiumBy.ID, DEPARTURE_AIRPORT, timeout=timeout)
        return self

    @property
    def departure_airport(self) -> str:
        """Departure airport IATA code, e.g. 'TLL'."""
        return self._text(DEPARTURE_AIRPORT)

    @property
    def arrival_airport(self) -> str:
        """Arrival airport IATA code, e.g. 'DUB'."""
        return self._text(ARRIVAL_AIRPORT)

    @property
    def departure_time(self) -> str:
        """Departure time in HH:MM format, e.g. '22:20'."""
        return self._text(DEPARTURE_TIME)

    @property
    def arrival_time(self) -> str:
        """Arrival time in HH:MM format, e.g. '23:35'."""
        return self._text(ARRIVAL_TIME)

    @property
    def flight_time(self) -> str:
        """Flight duration string, e.g. '3 h 15 m'."""
        return self._text(FLIGHT_TIME)

    @property
    def flight_number(self) -> str:
        """Flight number, e.g. 'FR 5694'."""
        return self._text(FLIGHT_NUMBER)

    @property
    def price(self) -> float:
        """Lowest fare price as a float (EUR), e.g. 29.91."""
        return float(self._text(PRICE))

    @property
    def currency(self) -> str:
        """Currency code, e.g. 'EUR'."""
        return self._text(CURRENCY)
