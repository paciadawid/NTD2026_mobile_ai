# Testing Guidelines

## Structure
- Tests are grouped by app inside `tests/<app>/`, e.g. `tests/ryanair/`, `tests/calculator/`.
- Pages are grouped by app inside `pages/<app>/`, e.g. `pages/ryanair/`, `pages/calculator/`.
- Each app subdirectory must contain an `__init__.py` (even if empty).
- `BasePage` lives at `pages/base_page.py` — shared across all apps.
- Test files are named `test_<feature>.py`.
- Test functions are named `test_<feature>_<scenario>`.
- The shared `driver` fixtures are defined in `conftest.py` at the project root.

## Page Object Model (POM)
- One class per physical screen — never merge multiple screens into one page object.
- All locators live in the page object (`pages/<app>/`) — never in test files.
- Page objects receive the `driver` in `__init__` and extend `BasePage`.
- Never instantiate page objects inside a test function. Use pytest fixtures instead.
- Static locators are always defined as module-level constants (before the class). Dynamic locators (f-strings with parameters) may remain inline in methods.

## Fixtures
- All driver fixtures are defined in `conftest.py` — do not redefine in test files.
- Every page object must have a corresponding pytest fixture in `conftest.py`.
- Fixtures inject page objects into tests — tests receive pages as parameters, not `driver`.
- The Ryanair driver is function-scoped with `no_reset=False` (fresh app state per test).
- Example:
  ```python
  # conftest.py
  @pytest.fixture
  def privacy_page(driver_ryanair):
      from pages.ryanair.privacy_page import PrivacyPage
      return PrivacyPage(driver_ryanair)

  # test file
  def test_foo(privacy_page, login_page, home_page):
      privacy_page.accept()
      login_page.continue_as_guest()
      ...
  ```

## Waits
- **Never use static waits** (`time.sleep`, `asyncio.sleep`, etc.).
- Use explicit waits only: `self._wait.until(EC.element_to_be_clickable(...))`.
- `self._wait` (15 s) is inherited from `BasePage` — do NOT create a new `WebDriverWait` inside a page method.
- For optional/conditional elements (e.g. permission dialogs), use `self._wait_short` (5 s) with `try/except`.
- Do not repeat `WebDriverWait(self._driver, N)` anywhere — use the pre-built instances from `BasePage`.

## Conventions
- Keep tests independent — each test must set up its own preconditions.
- Use `assert` statements directly (pytest-style); avoid unittest assertions.
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
