# Appium & Device Guidelines

## Appium Server
- Server URL: `http://127.0.0.1:4723`
- Must be started manually before running tests: `appium`
- Version: 3.x

## Default Capabilities (Android)
- `platformName`: `Android`
- `automationName`: `UiAutomator2`
- `deviceName`: `emulator-5554`
- `platformVersion`: `16` (API 36)
- `no_reset`: `True` — do not clear app data between sessions

## App Under Test
- Package: `com.google.android.calculator`
- Main activity: `com.android.calculator2.Calculator`
- Capabilities file: `capabilities.json`

## Key Element IDs — Calculator
Use `AppiumBy.ID` for resource IDs (short form — no package prefix) and `AppiumBy.ACCESSIBILITY_ID` for content descriptions.

| Element        | Locator strategy            | Value           |
|----------------|-----------------------------|-----------------|
| Clear (AC/CLR) | `AppiumBy.ID`               | `clr`           |
| Digit 0–9      | `AppiumBy.ID`               | `digit_<n>`     |
| Plus           | `AppiumBy.ID`               | `op_add`        |
| Minus          | `AppiumBy.ID`               | `op_sub`        |
| Multiply       | `AppiumBy.ID`               | `op_mul`        |
| Divide         | `AppiumBy.ID`               | `op_div`        |
| Equals         | `AppiumBy.ID`               | `eq`            |
| Result (final) | `AppiumBy.ID`               | `result_final`  |
| More options   | `AppiumBy.ACCESSIBILITY_ID` | `More options`  |

## Locator Strategy Priority
Use locators in this order — prefer the most stable and readable option:

1. **`AppiumBy.ID`** (`resource-id`) — use whenever the element has a unique resource ID. Fastest and most stable.
   - **Never include the package prefix** (`com.example:id/`). Appium UIAutomator2 automatically adds it. Write just the local part: `"container_search"`, not `"com.ryanair.cheapflights:id/container_search"`.
2. **`AppiumBy.ANDROID_UIAUTOMATOR`** — use for text-based lookups when no resource ID is available (e.g. Jetpack Compose screens):
   ```python
   'new UiSelector().text("Continue as guest")'
   'new UiSelector().className("android.widget.EditText")'
   'new UiSelector().className("android.view.View").clickable(true).enabled(true).instance(0)'
   ```
3. **`AppiumBy.XPATH`** — use only as a last resort. Avoid complex or positional XPath.
   - Never use positional XPath like `//android.widget.TextView[2]`.
   - Never use index-based selectors.

## Locator Placement
- All static locator strings must be defined as **module-level constants** (above the class definition).
- Dynamic locators (f-strings that embed test data) may remain inline in the method body.
- One `_UIA = AppiumBy.ANDROID_UIAUTOMATOR` alias per file reduces repetition when many UiSelector constants are used.

## BasePage Wait Helpers
All page objects extend `BasePage` which provides two pre-configured `WebDriverWait` instances:
- `self._wait` — 15 s, for required elements
- `self._wait_short` — 5 s, for optional/conditional elements (wrap in `try/except`)

**Never** create a new `WebDriverWait(self._driver, N)` inside a page method. Use the inherited helpers.

## Mobile MCP
- Package: `@mobilenext/mobile-mcp`
- Runs via `npx` — no global install needed.
- Connects directly to the device — no Appium server required.
- Device ID for emulator: `emulator-5554`
