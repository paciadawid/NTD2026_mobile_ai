# Project Guidelines — NTD2026 Mobile AI Workshop

## Project Overview
- AI-powered E2E mobile testing workshop using Appium and Mobile MCP.
- Language: **Python** (3.13 or 3.14).
- Test framework: **pytest**.
- Mobile automation: **Appium 3** with the **Appium-Python-Client** library.
- Target platform: **Android only** (no iOS).

## Tech Stack & Versions
- Python: 3.13 or 3.14
- Node.js: 24 LTS (required for Appium server and Mobile MCP)
- Java: JDK 25 LTS (`JAVA_HOME` must be set)
- Android: API 36 / Android 16 (`ANDROID_HOME` must be set)
- Appium: 3.x (installed globally via npm)
- Appium driver: **uiautomator2**
- Mobile MCP: runs via `npx` (not installed upfront)

## Key Dependencies
- `Appium-Python-Client` — Python client for Appium.
- `pytest` — test runner.
- `python-dotenv` — loads `.env` file into `os.environ` at startup.
- `ruff` — linter and formatter (dev only).

## Environment Variables
- `JAVA_HOME` — path to JDK 25 installation.
- `ANDROID_HOME` — path to Android SDK (macOS default: `~/Library/Android/sdk`).
- `PATH` must include `$ANDROID_HOME/platform-tools`, `$ANDROID_HOME/emulator`.
- `BROWSERSTACK_USERNAME` / `BROWSERSTACK_ACCESS_KEY` — BrowserStack credentials.
  - Locally: stored in `.env` (git-ignored). Copy `.env.example` and fill in real values.
  - CI: stored as GitHub repository secrets.

## Coding Rules
- All code must pass `ruff check` and `ruff format --check` before committing.
- Use Python type hints where practical.
- Target only Android — do not write iOS-specific code or capabilities.
