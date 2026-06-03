---
type: auto
description: Rules for Appium driver setup, Android capabilities, driver lifecycle, and explicit waits. Apply when creating or editing capability builders, conftest driver fixtures, or any code that initialises a WebDriver session.
---

# Appium Driver Rules

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
    "appium:avd": os.getenv("AVD_NAME"),          # e.g. "Pixel_9_2"
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
