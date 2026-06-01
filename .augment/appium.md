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
Use `AppiumBy.ID` for resource IDs and `AppiumBy.ACCESSIBILITY_ID` for content descriptions.

| Element        | Locator strategy        | Value                                            |
|----------------|-------------------------|--------------------------------------------------|
| Clear (AC/CLR) | `AppiumBy.ID`           | `com.google.android.calculator:id/clr`           |
| Digit 0–9      | `AppiumBy.ID`           | `com.google.android.calculator:id/digit_<n>`     |
| Plus           | `AppiumBy.ID`           | `com.google.android.calculator:id/op_add`        |
| Minus          | `AppiumBy.ID`           | `com.google.android.calculator:id/op_sub`        |
| Multiply       | `AppiumBy.ID`           | `com.google.android.calculator:id/op_mul`        |
| Divide         | `AppiumBy.ID`           | `com.google.android.calculator:id/op_div`        |
| Equals         | `AppiumBy.ID`           | `com.google.android.calculator:id/eq`            |
| Result (final) | `AppiumBy.ID`           | `com.google.android.calculator:id/result_final`  |
| More options   | `AppiumBy.ACCESSIBILITY_ID` | `More options`                               |

## Mobile MCP
- Package: `@mobilenext/mobile-mcp`
- Runs via `npx` — no global install needed.
- Connects directly to the device — no Appium server required.
- Device ID for emulator: `emulator-5554`
