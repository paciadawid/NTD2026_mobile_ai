---
type: always
---

# Mobile Testing Framework Rules

## Appium MCP
- **Always** use the `Appium MCP` to inspect the app UI and discover element locators before implementing or modifying Page Objects.
- **Before any implementation**, navigate through the full UI path that the test will follow — tap through every screen and state transition — then retrieve the page source at each step to discover resource-ids and content-descs.
- Use Appium MCP to retrieve the page source, find resource-ids, content-descs, and verify element availability at runtime.
- Prefer locators discovered via Appium MCP over guessed or assumed values — the live source reflects the actual app state.

## Stack
- **Language**: Python 3.9+
- **Test runner**: pytest
- **Automation**: Appium (Python client)
- **Platform**: Android only — never generate iOS capabilities or XCUITest references
- **Targets**: Android emulators and real physical devices
- **Remote execution**: BrowserStack (credentials via `.env`)

## Project structure
```
conftest.py          # root conftest: driver fixture, screenshot-on-failure hook
tests/               # one file per feature, named test_<feature>.py
pages/               # Page Object classes, one per screen
pages/base_page.py   # BasePage: shared driver wiring + primitive helpers (_tap, _get_text)
capabilities/        # capability builder helpers (emulator.py, real_device.py, browserstack.py)
utils/               # shared helpers: waits, scroll actions, gesture utilities
data/                # test data files (JSON/YAML), never credentials
reports/             # allure output directory (gitignored)
```

## Capabilities

### Required for every session
```python
{
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:app": app_path,   # passed as a parameter; resolved from APP_PATH env var in conftest.py
}
```

### Emulator additions
```python
{
    "appium:avd": os.getenv("AVD_NAME"),          # e.g. "Pixel_7_API_34"
    "appium:avdLaunchTimeout": 120000,
    "appium:isHeadless": False,
}
```

### Real device additions
```python
{
    "appium:udid": os.getenv("DEVICE_UDID"),      # from env, never hardcoded
    "appium:deviceName": os.getenv("DEVICE_NAME"),
}
```

### BrowserStack additions
```python
{
    "bstack:options": {
        "userName": os.getenv("BS_USERNAME"),
        "accessKey": os.getenv("BS_ACCESS_KEY"),
        "projectName": "NTD2026",
        "buildName": os.getenv("BUILD_NAME", "local"),
        "sessionName": "<test name>",
        "debug": True,
        "networkLogs": True,
    }
}
```

## Driver lifecycle
- Use **`scope="function"`** for the driver fixture — each test gets a clean session; this is the only safe default for stateful mobile UI tests
- `scope="session"` is only acceptable for a suite of strictly read-only smoke tests where all tests share identical preconditions; document the exception explicitly with a comment
- Never instantiate `webdriver.Remote` directly inside a test function
- Always call `driver.quit()` in the fixture teardown (`yield` pattern), even on failure

```python
@pytest.fixture(scope="function")
def driver(capabilities):
    drv = webdriver.Remote(appium_server_url(), capabilities)
    yield drv
    drv.quit()
```

## Screenshot on failure
- The root `conftest.py` **must** implement a `pytest_runtest_makereport` hook that captures a screenshot on any test failure
- Screenshots are saved to `reports/screenshots/` with the test node name as the filename
- The hook must handle the case where the driver is not available (e.g. failure during fixture setup)

```python
from pathlib import Path
import pytest

SCREENSHOT_DIR = Path("reports/screenshots")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            safe_name = item.nodeid.replace("/", "_").replace("::", "_")
            driver.get_screenshot_as_file(str(SCREENSHOT_DIR / f"{safe_name}.png"))
```

## Reporting
- Use **Allure** (`allure-pytest`) as the reporting framework
- Always pass `--alluredir=reports/allure-results` when running pytest — locally and in CI
- Serve the report locally with `allure serve reports/allure-results`
- Attach screenshots to the Allure report inside the failure hook using `allure.attach()`
- The `reports/` directory is gitignored; never commit generated reports

```python
import allure

# inside the failure hook, after saving the file:
allure.attach(
    driver.get_screenshot_as_png(),
    name=safe_name,
    attachment_type=allure.attachment_type.PNG,
)
```

### GitHub Actions
- Always upload Allure results as a GitHub Actions artifact after the test step
- Use `if: always()` so results are uploaded even when tests fail
- Name the artifact `allure-results-${{ github.run_number }}` for traceability
- Set `retention-days: 30` to keep results without bloating storage indefinitely
- Use the latest `actions/upload-artifact` (currently `v7`)

```yaml
- name: Run tests
  run: uv run pytest tests/ -v --tb=short --alluredir=reports/allure-results

- name: Upload Allure results
  if: always()
  uses: actions/upload-artifact@v7
  with:
    name: allure-results-${{ github.run_number }}
    path: reports/allure-results/
    retention-days: 30
```

To inspect a CI run locally, download the artifact from the GitHub Actions run page and run:
```sh
allure serve <path-to-downloaded-and-unzipped-artifact>
```

## Page Object Model
- Every screen has a dedicated class in `pages/` that inherits from `BasePage`
- Locators are class-level constants using `AppiumBy` (never raw strings)
- Methods return a new Page Object on navigation; action methods return `None` — prefer calling actions one per line over chaining
- No assertions inside Page Objects — assertions belong in tests
- **Never instantiate Page Objects inside test functions** — create them in fixtures and inject via the test signature

### BasePage — shared base for all Page Objects

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

### Concrete Page Object

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

## Locator priority (best to worst)
1. `AppiumBy.ID` (resource-id) — use the **short form** (e.g. `"digit_1"`), never the full `package:id/name` prefix; Appium/UiAutomator2 resolves the package automatically from the active session
2. `AppiumBy.ACCESSIBILITY_ID` (content-desc)
3. `AppiumBy.XPATH` — only when nothing else works; keep expressions short

## Waits
- Always use **explicit waits** (`WebDriverWait` + `expected_conditions`)
- Never use `time.sleep()`
- Never use `driver.implicitly_wait()` — mixing implicit and explicit waits causes unpredictable timeouts and is banned entirely
- **Never hardcode timeout values** — read from `WAIT_TIMEOUT` env var with a sensible default:
  ```python
  _DEFAULT_WAIT_TIMEOUT = int(os.getenv("WAIT_TIMEOUT", "10"))
  ```
- Page Object constructors accept a `timeout: int = _DEFAULT_WAIT_TIMEOUT` parameter so callers can override per-instance when needed
- Document `WAIT_TIMEOUT` in `.env.example`

## Naming conventions
| Thing | Convention | Example |
|---|---|---|
| Test files | `test_<feature>.py` | `test_login.py` |
| Test functions | `test_<action>_<expected_result>` | `test_login_with_valid_credentials_navigates_home` |
| Page classes | `<Screen>Page` | `LoginPage` |
| Fixture files | `conftest.py` at relevant directory level | — |
| Capability builders | `build_emulator_caps()` / `build_real_device_caps()` / `build_browserstack_caps()` | — |

## Environment variables
- All device identifiers, credentials, and paths come from `.env` via `python-dotenv`
- Never hardcode UDIDs, access keys, or file paths in source code
- `APP_PATH` is mandatory — capability builders receive it as an explicit parameter; `conftest.py` resolves it from the env and raises `ValueError` if it is not set
- `.env.example` documents every required variable — keep it in sync

## Pytest markers
Register custom markers in `pyproject.toml` to allow targeted runs:
```toml
[tool.pytest.ini_options]
markers = [
    "emulator: tests that run on Android emulators",
    "real_device: tests that run on physical Android devices",
    "browserstack: tests that execute on BrowserStack",
    "smoke: quick sanity suite",
    "regression: full regression suite",
]
```

## Code style
- Follow **PEP 8** in all Python files
- Maximum line length: **120 characters**
- Use **double quotes** for strings
- Use **4-space indentation**, never tabs
- Add a **blank line** between each test function and between Page Object methods
- All public functions, methods, and fixtures must have **type annotations**
- Imports order: standard library, then third-party, then local

## What NOT to do
- Do not use driver.find_element_by_* (deprecated Appium 1 API)
- Do not import from selenium.webdriver for mobile actions, use appium.webdriver
- Do not share a single driver instance across unrelated test classes
- Do not generate iOS-specific code (XCUITestDriver, bundleId, wdaLocalPort, etc.)
- Do not hardcode APP_PATH or any APK path inside capability builders — always receive it as a parameter
- Do not instantiate Page Objects inside test functions — always use fixtures
- Do not split a single logical check into multiple test functions — group related assertions in one test
- Do not commit or push passwords, API keys, access tokens, UDIDs, or any other credentials or sensitive data — always use `.env` and ensure `.env` is listed in `.gitignore`
- Do not hardcode credentials anywhere in source code, test files, capability builders, or config files — always read them from environment variables via `os.getenv()`
- Do not log, print, or expose sensitive values (tokens, passwords, access keys) in test output, reports, or screenshots
