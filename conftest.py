import os

import allure
import pytest
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options
from dotenv import load_dotenv

load_dotenv()  # loads .env into os.environ; no-op when absent (e.g. CI uses secrets)

# ── Appium hubs ───────────────────────────────────────────────────────────────
LOCAL_HUB = "http://127.0.0.1:4723"
BROWSERSTACK_HUB = "https://hub-cloud.browserstack.com/wd/hub"

# ── Local emulator ────────────────────────────────────────────────────────────
LOCAL_DEVICE = os.environ.get("LOCAL_DEVICE", "emulator-5554")

# ── BrowserStack shared ───────────────────────────────────────────────────────
BS_DEVICE = "Google Pixel 10"
BS_OS_VERSION = "16.0"
BS_PROJECT = "NTD2026 Mobile AI Workshop"

# ── Google Calculator ─────────────────────────────────────────────────────────
CALC_PACKAGE = "com.google.android.calculator"
CALC_ACTIVITY = "com.android.calculator2.Calculator"
CALC_BS_APP_ID = "GoogleCalculator"  # custom_id uploaded to BrowserStack
CALC_BS_BUILD = "Calculator Tests"

# ── Sauce Labs My Demo App (MDA) ──────────────────────────────────────────────
MDA_PACKAGE = "com.saucelabs.mydemoapp.android"
MDA_ACTIVITY = "com.saucelabs.mydemoapp.android.view.activities.SplashActivity"
MDA_BS_APP_ID = "SauceLabs_MDA"  # custom_id — upload app/mda-2.2.0-25.apk to BrowserStack first
MDA_BS_BUILD = "Shop Tests"

# ── Ryanair ───────────────────────────────────────────────────────────────────
RYANAIR_PACKAGE = "com.ryanair.cheapflights"
RYANAIR_ACTIVITY = "com.ryanair.cheapflights.ui.SplashScreenActivity"
RYANAIR_BS_APP_ID = "Ryanair"  # custom_id — upload the Ryanair APK to BrowserStack first
RYANAIR_BS_BUILD = "Ryanair Flight Search Tests"


def _local_options(package: str, activity: str, *, no_reset: bool = True) -> UiAutomator2Options:
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = LOCAL_DEVICE
    options.app_package = package
    options.app_activity = activity
    options.no_reset = no_reset
    return options


def _browserstack_options(
    package: str,
    activity: str,
    app_id: str,
    build_name: str,
    session_name: str,
    *,
    no_reset: bool = True,
) -> UiAutomator2Options:
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.app_package = package
    options.app_activity = activity
    options.no_reset = no_reset
    options.set_capability("app", app_id)
    options.set_capability(
        "bstack:options",
        {
            "userName": os.environ["BROWSERSTACK_USERNAME"],
            "accessKey": os.environ["BROWSERSTACK_ACCESS_KEY"],
            "deviceName": BS_DEVICE,
            "osVersion": BS_OS_VERSION,
            "projectName": BS_PROJECT,
            "buildName": build_name,
            "sessionName": session_name,
        },
    )
    return options


def _make_driver(
    package: str,
    activity: str,
    app_id: str,
    build_name: str,
    default_session_name: str,
    *,
    no_reset: bool = True,
):
    """Create and return a configured Appium WebDriver (local or BrowserStack)."""
    use_bs = os.environ.get("BS_TARGET", "").lower() in ("1", "true", "yes")

    if use_bs:
        username = os.environ.get("BROWSERSTACK_USERNAME")
        access_key = os.environ.get("BROWSERSTACK_ACCESS_KEY")
        if not username or not access_key:
            pytest.exit(
                "BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY must be set when BS_TARGET=1. "
                "Add them to .env locally or as GitHub Secrets in CI.",
                returncode=2,
            )

    hub = BROWSERSTACK_HUB if use_bs else LOCAL_HUB
    if use_bs:
        session_name = os.environ.get("BS_SESSION_NAME", default_session_name)
        options = _browserstack_options(package, activity, app_id, build_name, session_name, no_reset=no_reset)
    else:
        options = _local_options(package, activity, no_reset=no_reset)

    return webdriver.Remote(hub, options=options)


@pytest.fixture(scope="module")
def driver():
    """Appium WebDriver for Google Calculator.

    Set BS_TARGET=1 to run on BrowserStack instead of a local emulator.
    """
    d = _make_driver(CALC_PACKAGE, CALC_ACTIVITY, CALC_BS_APP_ID, CALC_BS_BUILD, "Calculator Test Run")
    yield d
    d.quit()


@pytest.fixture
def driver_mda():
    """Appium WebDriver for Sauce Labs My Demo App.

    Function-scoped (one session per test) so no_reset=False cleanly wipes the cart
    and app state before every test without any manual reset logic.

    Set BS_TARGET=1 to run on BrowserStack instead of a local emulator.
    Upload app/mda-2.2.0-25.apk to BrowserStack with custom_id=SauceLabs_MDA before running remotely.
    """
    d = _make_driver(MDA_PACKAGE, MDA_ACTIVITY, MDA_BS_APP_ID, MDA_BS_BUILD, "Shop Test Run", no_reset=False)
    yield d
    d.quit()


@pytest.fixture
def product_list_page(driver_mda):
    """Ready-to-use ProductListPage bound to the MDA driver."""
    from pages.shop.product_list_page import ProductListPage

    return ProductListPage(driver_mda)


@pytest.fixture
def calculator_page(driver):
    """Ready-to-use CalculatorPage bound to the Calculator driver.

    Clears the calculator before each test so module-scoped driver state never
    leaks between tests.
    """
    from pages.calculator.calculator_page import CalculatorPage

    page = CalculatorPage(driver)
    page.clear()
    return page


@pytest.fixture
def driver_ryanair():
    """Appium WebDriver for the Ryanair app.

    Function-scoped with no_reset=False so every test starts from a clean app state
    (privacy screen, fresh session — no cached login or promo dismissal).

    Set BS_TARGET=1 to run on BrowserStack instead of a local emulator.
    """
    d = _make_driver(
        RYANAIR_PACKAGE,
        RYANAIR_ACTIVITY,
        RYANAIR_BS_APP_ID,
        RYANAIR_BS_BUILD,
        "Ryanair Flight Search",
        no_reset=False,
    )
    yield d
    d.quit()


# ── Ryanair page fixtures ─────────────────────────────────────────────────────

@pytest.fixture
def privacy_page(driver_ryanair):
    from pages.ryanair.privacy_page import PrivacyPage
    return PrivacyPage(driver_ryanair)


@pytest.fixture
def login_page(driver_ryanair):
    from pages.ryanair.login_page import LoginPage
    return LoginPage(driver_ryanair)


@pytest.fixture
def home_page(driver_ryanair):
    from pages.ryanair.home_page import HomePage
    return HomePage(driver_ryanair)


@pytest.fixture
def find_flights_page(driver_ryanair):
    from pages.ryanair.find_flights_page import FindFlightsPage
    return FindFlightsPage(driver_ryanair)


@pytest.fixture
def airport_picker_page(driver_ryanair):
    from pages.ryanair.airport_picker_page import AirportPickerPage
    return AirportPickerPage(driver_ryanair)


@pytest.fixture
def date_picker_page(driver_ryanair):
    from pages.ryanair.date_picker_page import DatePickerPage
    return DatePickerPage(driver_ryanair)


@pytest.fixture
def results_page(driver_ryanair):
    from pages.ryanair.results_page import RyanairResultsPage
    return RyanairResultsPage(driver_ryanair)


# ── Screenshot on failure ─────────────────────────────────────────────────────

DIAGNOSTICS_DIR = "diagnostics"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """On test-call failure: attach to Allure AND save screenshot + page XML to /diagnostics."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = (
            item.funcargs.get("driver")
            or item.funcargs.get("driver_mda")
            or item.funcargs.get("driver_ryanair")
        )
        if driver:
            # ── Allure attachment (existing behaviour) ────────────────────────
            png_bytes = driver.get_screenshot_as_png()
            allure.attach(
                png_bytes,
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )

            # ── Persist to /diagnostics folder ────────────────────────────────
            os.makedirs(DIAGNOSTICS_DIR, exist_ok=True)
            safe_name = item.nodeid.replace("/", "_").replace("::", "__")

            screenshot_path = os.path.join(DIAGNOSTICS_DIR, f"{safe_name}.png")
            with open(screenshot_path, "wb") as f:
                f.write(png_bytes)

            xml_path = os.path.join(DIAGNOSTICS_DIR, f"{safe_name}.xml")
            with open(xml_path, "w", encoding="utf-8") as f:
                f.write(driver.page_source)

            print(f"\n[diagnostics] screenshot → {screenshot_path}")
            print(f"[diagnostics] page XML   → {xml_path}")
