"""
Ryanair App Explorer - finds first available flight from Tallinn to Dublin.
Run: python explore_ryanair.py
"""
import time
import json
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

APPIUM_URL = "http://127.0.0.1:4723"
PACKAGE = "com.ryanair.cheapflights"
ACTIVITY = "com.ryanair.cheapflights.ui.SplashScreenActivity"


def make_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "emulator-5554"
    options.app_package = PACKAGE
    options.app_activity = ACTIVITY
    options.no_reset = False   # fresh app state
    options.auto_grant_permissions = True
    return webdriver.Remote(APPIUM_URL, options=options)


def wait_for(driver, by, value, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def find_opt(driver, by, value):
    try:
        return driver.find_element(by, value)
    except NoSuchElementException:
        return None


def screenshot_and_source(driver, name):
    driver.save_screenshot(f"diagnostics/ryanair_{name}.png")
    with open(f"diagnostics/ryanair_{name}.xml", "w") as f:
        f.write(driver.page_source)
    print(f"[snapshot] {name}")


def dismiss_popups(driver):
    """Dismiss common popups: cookie consent, notifications, location, onboarding."""
    popup_xpaths = [
        # Ryanair privacy consent
        '//*[@text="Yes, I agree"]',
        '//*[@text="No, thanks"]',
        # Generic accept/allow
        '//*[@text="Accept" or @text="ACCEPT" or @text="Accept all"]',
        '//*[@text="Allow" or @text="ALLOW"]',
        '//*[@text="Got it" or @text="GOT IT"]',
        '//*[@text="Skip" or @text="SKIP"]',
        '//*[@text="Continue" or @text="CONTINUE"]',
        '//*[@text="No thanks" or @text="No Thanks"]',
        '//*[@resource-id="com.ryanair.cheapflights:id/close_button"]',
        '//*[@content-desc="Close" or @content-desc="close"]',
        '//*[@text="OK" or @text="Ok"]',
        '//*[@text="Done" or @text="DONE"]',
    ]
    dismissed = 0
    for xpath in popup_xpaths:
        el = find_opt(driver, AppiumBy.XPATH, xpath)
        if el:
            try:
                el.click()
                dismissed += 1
                print(f"  dismissed: {xpath}")
                time.sleep(1.5)
            except Exception:
                pass
    return dismissed


def tap_one_way(driver):
    """Switch to one-way trip if not already."""
    for xpath in [
        '//*[@text="One way" or @text="ONE WAY" or @text="One Way"]',
        '//*[contains(@text,"one way") or contains(@text,"One way")]',
    ]:
        el = find_opt(driver, AppiumBy.XPATH, xpath)
        if el:
            el.click()
            print("  selected one-way")
            time.sleep(1)
            return


def set_airport(driver, field_hint, airport_code, airport_name):
    """Click airport field, type search, pick first matching result."""
    # Try to find the From/To field by hint text or resource-id
    for xpath in [
        f'//*[contains(@text,"{field_hint}") or contains(@hint,"{field_hint}")]',
        f'//*[@resource-id="com.ryanair.cheapflights:id/{field_hint.lower()}_airport"]',
    ]:
        el = find_opt(driver, AppiumBy.XPATH, xpath)
        if el:
            el.click()
            time.sleep(1.5)
            break

    # Type the airport code
    active = find_opt(driver, AppiumBy.XPATH, '//*[@focused="true"]')
    if active:
        active.send_keys(airport_code)
    else:
        driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText").send_keys(airport_code)

    time.sleep(2)
    # Pick first result matching airport name
    for xpath in [
        f'//*[contains(@text,"{airport_name}")]',
        f'//*[contains(@text,"{airport_code}")]',
    ]:
        el = find_opt(driver, AppiumBy.XPATH, xpath)
        if el:
            el.click()
            print(f"  selected {airport_code} - {airport_name}")
            time.sleep(1)
            return
    print(f"  WARNING: could not find {airport_code} in suggestions")


def main():
    import os
    os.makedirs("diagnostics", exist_ok=True)

    print("Starting Appium session (fresh Ryanair state)...")
    driver = make_driver()
    wait = WebDriverWait(driver, 20)

    try:
        print("Waiting for app to load...")
        time.sleep(8)
        screenshot_and_source(driver, "01_after_launch")

        print("Dismissing popups...")
        for _ in range(4):
            dismiss_popups(driver)
            time.sleep(1.5)

        screenshot_and_source(driver, "02_after_popups")

        print("Looking for home / search screen...")
        time.sleep(2)
        dismiss_popups(driver)
        screenshot_and_source(driver, "03_home")

        print("Switching to one-way...")
        tap_one_way(driver)
        screenshot_and_source(driver, "04_one_way")

        print("Setting departure: Tallinn (TLL)...")
        set_airport(driver, "From", "TLL", "Tallinn")
        screenshot_and_source(driver, "05_from_tallinn")

        print("Setting destination: Dublin (DUB)...")
        set_airport(driver, "To", "DUB", "Dublin")
        screenshot_and_source(driver, "06_to_dublin")

        print("Looking for date picker...")
        screenshot_and_source(driver, "07_before_date")

    finally:
        print("\nPage source saved. Session ending.")
        driver.quit()


if __name__ == "__main__":
    main()
