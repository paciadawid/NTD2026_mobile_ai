# Testing Guidelines

## Structure
- All tests live in the `tests/` directory.
- Test files are named `test_<feature>.py`.
- Test functions are named `test_<feature>_<scenario>`.
- The shared `driver` fixture is defined in `conftest.py` at the project root.

## Fixtures
- Use the `driver` fixture from `conftest.py` — do not redefine it in test files.
- Fixture scope is `module` — one Appium session per test file.
- Use `CalculatorPage(driver)` from `pages/calculator_page.py` — never call `find_element` directly in tests.

## Conventions
- Keep tests independent — each test must set up its own preconditions (call `calc.clear()` first).
- Use `assert` statements directly (pytest-style); avoid unittest assertions.
- Locators live in the Page Object (`pages/`) — never in test files.
- Mark critical path tests with `@pytest.mark.smoke`.

## Running Tests
```
# Run locally (Appium server must be running first: appium)
uv run pytest tests/ -v

# Run on BrowserStack (credentials must be set as env vars)
BS_TARGET=1 uv run pytest tests/ -v
```

## BrowserStack
- Enabled by setting `BS_TARGET=1` (or `true`/`yes`) environment variable.
- Credentials are read from `BROWSERSTACK_USERNAME` and `BROWSERSTACK_ACCESS_KEY` env vars.
- Store credentials in `.env` locally (git-ignored); use GitHub Secrets in CI.
- Target device: Google Pixel 10, Android 16.0.
- APK is stored locally in `app/calculator.apk` (git-ignored — do not commit).
- App uploaded as custom_id `GoogleCalculator` — re-upload with `curl` if it expires (60 days):
  ```
  curl -u "$BROWSERSTACK_USERNAME:$BROWSERSTACK_ACCESS_KEY" \
    -X POST "https://api-cloud.browserstack.com/app-automate/upload" \
    -F "file=@app/calculator.apk" -F "custom_id=GoogleCalculator"
  ```
- Hub URL: `https://hub-cloud.browserstack.com/wd/hub`
- Never hardcode credentials in test code.
