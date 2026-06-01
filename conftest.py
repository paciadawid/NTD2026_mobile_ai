import os

import pytest
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options
from dotenv import load_dotenv

load_dotenv()  # loads .env into os.environ; no-op when absent (e.g. CI uses secrets)

# ── Appium hubs ───────────────────────────────────────────────────────────────
LOCAL_HUB = "http://127.0.0.1:4723"
BROWSERSTACK_HUB = "https://hub-cloud.browserstack.com/wd/hub"

# ── App under test ────────────────────────────────────────────────────────────
APP_PACKAGE = "com.google.android.calculator"
APP_ACTIVITY = "com.android.calculator2.Calculator"

# ── Local emulator ────────────────────────────────────────────────────────────
LOCAL_DEVICE = "emulator-5554"

# ── BrowserStack ──────────────────────────────────────────────────────────────
BS_APP_ID = "GoogleCalculator"  # custom_id set when uploading the APK
BS_DEVICE = "Google Pixel 10"
BS_OS_VERSION = "16.0"
BS_PROJECT = "NTD2026 Mobile AI Workshop"
BS_BUILD = "Calculator Tests"


def _local_options() -> UiAutomator2Options:
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = LOCAL_DEVICE
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY
    options.no_reset = True
    return options


def _browserstack_options() -> UiAutomator2Options:
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY
    options.no_reset = True
    options.set_capability("app", BS_APP_ID)
    session_name = os.environ.get("BS_SESSION_NAME", "Calculator Test Run")
    options.set_capability(
        "bstack:options",
        {
            "userName": os.environ["BROWSERSTACK_USERNAME"],
            "accessKey": os.environ["BROWSERSTACK_ACCESS_KEY"],
            "deviceName": BS_DEVICE,
            "osVersion": BS_OS_VERSION,
            "projectName": BS_PROJECT,
            "buildName": BS_BUILD,
            "sessionName": session_name,
        },
    )
    return options


@pytest.fixture(scope="module")
def driver():
    """Yield an Appium WebDriver session and quit it after the module finishes.

    Set BS_TARGET=1 to run on BrowserStack instead of a local emulator.
    Credentials are read from BROWSERSTACK_USERNAME / BROWSERSTACK_ACCESS_KEY
    (populated from .env locally; from GitHub Secrets in CI).
    """
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
    options = _browserstack_options() if use_bs else _local_options()

    d = webdriver.Remote(hub, options=options)
    yield d
    d.quit()
