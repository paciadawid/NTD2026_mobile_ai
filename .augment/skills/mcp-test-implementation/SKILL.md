---
name: mcp-test-implementation
description: Step-by-step workflow for implementing an Appium test using Appium MCP or Mobile MCP with a diagnostics-first approach. Walks the full test scenario via MCP before writing any code, dumping page source and screenshots at every step.
---

# MCP-First Test Implementation Workflow

## Guiding principle
**Never write or modify a single line of test or page-object code before walking the full test path live via MCP and confirming every step works.**
Code follows evidence; evidence comes from MCP.

---

## Phase 1 — Explore the path via MCP (no code yet)

Execute every step the test will take, in the exact order the test will execute them.
At **each** step:

1. Call the MCP action (`tap_element`, `send_keys`, `swipe`, …).
2. Immediately call `get_page_source` to capture the live DOM.
3. Save the raw XML to `diagnostics/<feature>_step_<N>_<description>.xml`.
4. Call `take_screenshot` and save to `diagnostics/<feature>_step_<N>_<description>.png`.
5. Identify the best locator for every element touched or asserted on:
   - First choice: `resource-id` short form — e.g. `"digit_1"`, never the full `package:id/name` prefix
   - Second choice: `content-desc` (accessibility ID)
   - Last resort: XPath — keep expressions short
6. Record findings before moving to the next step.

Do **not** skip steps. Do **not** assume a locator from a previous screen is still valid.

### MCP tool quick reference

| Action | Tool name |
|---|---|
| Get live DOM | `get_page_source` |
| Screenshot | `take_screenshot` |
| Tap element | `tap_element` |
| Type text | `send_keys` |
| Swipe / scroll | `swipe` |
| Read attribute | `get_element_attribute` |

---

## Phase 2 — Verify end-to-end via MCP

After all individual steps pass, replay the **entire** sequence from app launch to the
final assertion element without stopping.

- Confirm the expected result element is visible and shows the correct text/state.
- If anything fails: open the saved XML for that step, find the real locator, fix your
  understanding, and repeat only that step in Phase 1. Never guess; never retry blind.
- Only move to Phase 3 after a clean, uninterrupted end-to-end MCP run.

---

## Phase 3 — Write the code (only after Phase 2 passes)

### 3a — Page Object locators
Use **only** resource-ids and content-descs confirmed by `get_page_source` in Phase 1.

```python
# pages/example_page.py
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class ExamplePage(BasePage):
    # locators confirmed via get_page_source in Phase 1
    BTN_SUBMIT = (AppiumBy.ID, "submit_button")          # resource-id short form
    LBL_RESULT = (AppiumBy.ACCESSIBILITY_ID, "result")   # content-desc fallback

    def tap_submit(self) -> None:
        self._tap(self.BTN_SUBMIT)

    def get_result(self) -> str:
        return self._get_text(self.LBL_RESULT)
```

### 3b — Page Object methods
Mirror the exact sequence of MCP actions observed in Phase 1.
Map each MCP call to the matching `BasePage` helper: `_tap` → tap, `_get_text` → read text.

### 3c — Test function
Follow the naming convention `test_<action>_<expected_result>`.
Inject the Page Object via fixture — never instantiate it inside the test function.

```python
# tests/test_example.py
import pytest
from pages.example_page import ExamplePage

@pytest.mark.regression
def test_submit_shows_result(example_page: ExamplePage) -> None:
    """Verify that tapping Submit displays the expected result."""
    example_page.tap_submit()
    assert example_page.get_result() == "OK", "Expected 'OK' after submit"
```

---

## Diagnostics rules

- `diagnostics/<feature>_step_<N>_<description>.xml` — page source at each MCP step
- `diagnostics/<feature>_step_<N>_<description>.png` — screenshot at each MCP step
- On any unexpected MCP behaviour: read the XML **first**, then retry — never guess.
- The `conftest.py` failure hook already writes `diagnostics/<safe_name>.xml/.png` on test
  failure; MCP exploration artifacts go in the same directory so all evidence is co-located.
- `diagnostics/` is gitignored — never commit these files.

---

## Pre-PR checklist

- [ ] Every locator was confirmed by `get_page_source` during Phase 1.
- [ ] A clean end-to-end MCP run completed without errors (Phase 2).
- [ ] Diagnostics XMLs for all steps exist in `diagnostics/` and were reviewed.
- [ ] No `time.sleep()` or `implicitly_wait()` in new or modified code.
- [ ] No hardcoded UDIDs, APK paths, or credentials.
- [ ] New pytest markers registered in `pyproject.toml` if added.
