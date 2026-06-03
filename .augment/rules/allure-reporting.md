---
type: auto
description: Rules for Allure reporting setup, screenshot-on-failure hook, and attaching artifacts. Apply when editing conftest.py, adding or modifying the pytest_runtest_makereport hook, or configuring allure-pytest.
---

# Allure Reporting Rules

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
            allure.attach(
                driver.get_screenshot_as_png(),
                name=safe_name,
                attachment_type=allure.attachment_type.PNG,
            )
```
