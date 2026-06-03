import os
from pathlib import Path

from appium.options.android import UiAutomator2Options


def build_browserstack_caps(app_path: str, session_name: str = "NTD2026 Test") -> UiAutomator2Options:
    """Build Appium capabilities for a BrowserStack remote session.

    The app is resolved in priority order:
      1. BROWSERSTACK_APP_URL env var — a bs:// URL from a previous upload (preferred).
      2. app_path argument           — uploaded on-the-fly by BrowserStack if a local path.
    """
    options = UiAutomator2Options()
    bs_app_url = os.getenv("BROWSERSTACK_APP_URL")
    options.app = (
        bs_app_url if bs_app_url else (app_path if app_path.startswith("bs://") else str(Path(app_path).resolve()))
    )
    options.device_name = os.getenv("BROWSERSTACK_DEVICE", "Google Pixel 7")
    options.platform_version = os.getenv("BROWSERSTACK_OS_VERSION", "13.0")
    options.set_capability(
        "bstack:options",
        {
            "userName": os.getenv("BS_USERNAME"),
            "accessKey": os.getenv("BS_ACCESS_KEY"),
            "projectName": "NTD2026",
            "buildName": os.getenv("BUILD_NAME", "local"),
            "sessionName": session_name,
            "debug": True,
            "networkLogs": True,
        },
    )
    print(options.get_capability("bstack:options"))
    return options
