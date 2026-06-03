import os
from pathlib import Path

from appium.options.android import UiAutomator2Options


def build_emulator_caps(app_path: str) -> UiAutomator2Options:
    """Build Appium capabilities for an Android emulator session."""
    options = UiAutomator2Options()
    options.app = str(Path(app_path).resolve())
    options.avd = os.getenv("AVD_NAME")
    options.avd_launch_timeout = 120000
    return options
