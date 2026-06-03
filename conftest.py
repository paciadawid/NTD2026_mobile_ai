import os
from collections.abc import Generator
from pathlib import Path

import allure
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv

from capabilities.browserstack import build_browserstack_caps
from capabilities.emulator import build_emulator_caps
from capabilities.real_device import build_real_device_caps

load_dotenv()

SCREENSHOT_DIR = Path("reports/screenshots")
DIAGNOSTICS_DIR = Path("diagnostics")

_BUILDERS = {
    "emulator": lambda app_path, name: build_emulator_caps(app_path),
    "real_device": lambda app_path, name: build_real_device_caps(app_path),
    "browserstack": lambda app_path, name: build_browserstack_caps(app_path, session_name=name),
}


def appium_server_url() -> str:
    """Return the Appium server URL for the current TARGET.

    BrowserStack uses its own fixed hub; all other targets resolve from env vars.
    """
    if os.getenv("TARGET", "emulator").lower() == "browserstack":
        return "https://hub-cloud.browserstack.com/wd/hub"
    host = os.getenv("APPIUM_HOST", "127.0.0.1")
    port = os.getenv("APPIUM_PORT", "4723")
    return f"http://{host}:{port}"


def _resolve_app_path() -> str:
    """Read APP_PATH from the environment; raise clearly if it is not set."""
    app_path = os.getenv("APP_PATH")
    if not app_path:
        raise ValueError("APP_PATH environment variable is not set. Add it to your .env file.")
    return app_path


def _build_caps(target: str, app_path: str, session_name: str) -> UiAutomator2Options:
    """Dispatch to the right capability builder based on TARGET."""
    builder = _BUILDERS.get(target)
    if builder is None:
        valid = ", ".join(_BUILDERS)
        raise ValueError(f"Unknown TARGET '{target}'. Must be one of: {valid}.")
    return builder(app_path, session_name)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator[None, None, None]:
    """Capture a screenshot and page source on any test failure.

    Artifacts are written to two locations:
      - reports/screenshots/<safe_name>.png   — screenshot for Allure
      - diagnostics/<safe_name>.png           — screenshot for quick inspection
      - diagnostics/<safe_name>.xml           — driver.page_source for DOM debugging
    The screenshot is also attached inline to the Allure report.
    """
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            safe_name = item.nodeid.replace("/", "_").replace("::", "_")

            # ── Allure screenshot (reports/screenshots/) ──────────────────────
            SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            driver.get_screenshot_as_file(str(SCREENSHOT_DIR / f"{safe_name}.png"))
            screenshot_bytes = driver.get_screenshot_as_png()
            allure.attach(
                screenshot_bytes,
                name=safe_name,
                attachment_type=allure.attachment_type.PNG,
            )

            # ── Diagnostics artifacts (diagnostics/) ──────────────────────────
            DIAGNOSTICS_DIR.mkdir(parents=True, exist_ok=True)
            (DIAGNOSTICS_DIR / f"{safe_name}.png").write_bytes(screenshot_bytes)
            (DIAGNOSTICS_DIR / f"{safe_name}.xml").write_text(
                driver.page_source, encoding="utf-8"
            )


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest) -> Generator[webdriver.Remote, None, None]:
    """Create an Appium driver session and tear it down after each test.

    The session target is controlled by the TARGET environment variable:
        emulator    — local Android emulator  (default)
        real_device — physical device via USB
        browserstack — BrowserStack Automate
    """
    target = os.getenv("TARGET", "emulator").lower()
    app_path = _resolve_app_path()
    caps = _build_caps(target, app_path=app_path, session_name=request.node.name)

    drv = webdriver.Remote(command_executor=appium_server_url(), options=caps)
    yield drv
    drv.quit()
