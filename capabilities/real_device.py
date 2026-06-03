import os
from pathlib import Path

from appium.options.android import UiAutomator2Options


def build_real_device_caps(app_path: str) -> UiAutomator2Options:
    """Build Appium capabilities for a real physical Android device session."""
    options = UiAutomator2Options()
    options.app = str(Path(app_path).resolve())
    options.udid = os.getenv("DEVICE_UDID")
    options.device_name = os.getenv("DEVICE_NAME")
    return options
