---
type: always
---

# Pytest Execution Rules

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

## Retries
- Use **`pytest-rerunfailures`** to automatically retry flaky tests
- Configure retries in `pyproject.toml` so they apply to every `pytest` invocation without extra CLI flags:
  ```toml
  [tool.pytest.ini_options]
  reruns = 2
  reruns_delay = 5
  ```
- `reruns = 2` — up to 2 retries per failing test
- `reruns_delay = 5` — 5-second pause between attempts, giving BrowserStack time to tear down the previous session
- `pytest-rerunfailures` is fully compatible with `pytest-xdist` (version ≥ 13)

## Parallel execution
- Use **`pytest-xdist`** for parallel test execution
- Do **not** set `-n` globally in `pyproject.toml` — it would break local emulator runs where only one device is available
- Add `-n <workers>` only in CI commands targeting BrowserStack:
  ```yaml
  run: uv run pytest tests/ -v --tb=short --alluredir=reports/allure-results -n 5
  ```
- The driver fixture **must** use `scope="function"` for parallel runs to work — each xdist worker gets its own independent driver session with no shared state
