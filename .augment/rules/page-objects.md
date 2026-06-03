---
type: auto
description: Rules for the Page Object Model pattern — BasePage, locator strategy, and interaction helpers. Apply when creating or editing any class in pages/, adding new locators, or implementing screen interactions.
---

# Page Object Model Rules

## Page Object Model
- Every screen has a dedicated class in `pages/` that inherits from `BasePage`
- Locators are class-level constants using `AppiumBy` (never raw strings)
- Methods return a new Page Object on navigation; action methods return `None` — prefer calling actions one per line over chaining
- No assertions inside Page Objects — assertions belong in tests
- **Never instantiate Page Objects inside test functions** — create them in fixtures and inject via the test signature

## Locator priority (best to worst)
1. `AppiumBy.ID` (resource-id) — use the **short form** (e.g. `"digit_1"`), never the full `package:id/name` prefix; Appium/UiAutomator2 resolves the package automatically from the active session
2. `AppiumBy.ACCESSIBILITY_ID` (content-desc)
3. `AppiumBy.XPATH` — only when nothing else works; keep expressions short

## BasePage — shared base for all Page Objects

`pages/base_page.py` holds all driver wiring and primitive interaction helpers. Every concrete Page Object inherits from it — never duplicate `__init__`, `_wait`, or interaction primitives in subclasses.

```python
# pages/base_page.py
import os

from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

_DEFAULT_WAIT_TIMEOUT = int(os.getenv("WAIT_TIMEOUT", "10"))


class BasePage:
    def __init__(self, driver: webdriver.Remote, timeout: int = _DEFAULT_WAIT_TIMEOUT) -> None:
        self.driver = driver
        self._wait = WebDriverWait(driver, timeout)

    def _tap(self, locator: tuple[str, str]) -> None:
        """Wait for *locator* to be clickable, then tap it."""
        self._wait.until(EC.element_to_be_clickable(locator)).click()

    def _get_text(self, locator: tuple[str, str]) -> str:
        """Wait for *locator* to be visible and return its text."""
        return self._wait.until(EC.visibility_of_element_located(locator)).text
```

## Concrete Page Object

```python
# pages/login_page.py
from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (AppiumBy.ID, "username")
    PASSWORD = (AppiumBy.ID, "password")
    LOGIN_BTN = (AppiumBy.ID, "login")

    def login(self, user: str, password: str) -> "HomePage":
        self._tap(self.USERNAME)   # or send_keys via driver directly
        self.driver.find_element(*self.USERNAME).send_keys(user)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self._tap(self.LOGIN_BTN)
        return HomePage(self.driver)
```
