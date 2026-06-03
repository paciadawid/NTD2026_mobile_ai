---
type: always
---

# Project Conventions

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

## Code style
- Follow **PEP 8** in all Python files
- Maximum line length: **120 characters**
- Use **double quotes** for strings
- Use **4-space indentation**, never tabs
- Add a **blank line** between each test function and between Page Object methods
- All public functions, methods, and fixtures must have **type annotations**
- Imports order: standard library, then third-party, then local
- Do **not** add inline comments that restate what the code already says — well-named methods and variables are self-documenting; only add a comment when it explains *why*, not *what*

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
