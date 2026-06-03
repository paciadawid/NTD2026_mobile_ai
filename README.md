# NTD2026 — AI-Powered Mobile Testing with Appium

A Python/Appium framework for Android UI test automation, built for the **NTD 2026 workshop on AI-powered E2E mobile testing**. Tests run against a local emulator, a physical device, or BrowserStack — selected by a single env var. AI agents accelerate every phase of the workflow via MCP servers wired directly into the IDE.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Running Tests](#running-tests)
4. [Tooling](#tooling)
5. [Framework Architecture](#framework-architecture)
6. [AI Usage and MCP Servers](#ai-usage-and-mcp-servers)

---

## Prerequisites

| Tool | Version | Notes |
|---|---|---|
| Python | 3.9+ (3.14 recommended) | |
| Node.js | 24 LTS | Required by Appium and MCP servers |
| Java JDK | 25 LTS | Set `JAVA_HOME` |
| Android Studio | Latest | Set `ANDROID_HOME`; create an API 36 AVD |
| Appium | 3.x | `npm i -g appium@latest` |
| UiAutomator2 driver | Latest | `appium driver install uiautomator2` |
| uv | Latest | Python package manager used in this project |

Verify your environment:

```sh
appium driver doctor uiautomator2   # everything should be green
adb --version
emulator -list-avds                 # your AVD must appear
```

---

## Setup

### 1. Clone and install dependencies

```sh
git clone <repo-url>
cd NTD2026_mobile_ai
uv sync                             # installs all deps from uv.lock
```

### 2. Configure environment variables

```sh
cp .env.example .env
# Edit .env — see the reference table below
```

| Variable | Required | Description |
|---|---|---|
| `APP_PATH` | ✅ Always | Absolute path to the APK under test |
| `TARGET` | ✅ Always | `emulator` (default) · `real_device` · `browserstack` |
| `APPIUM_HOST` | ✅ Always | Appium server host (default `127.0.0.1`) |
| `APPIUM_PORT` | ✅ Always | Appium server port (default `4723`) |
| `WAIT_TIMEOUT` | ✅ Always | Explicit wait timeout in seconds (default `10`) |
| `AVD_NAME` | When `TARGET=emulator` | Name of the Android Virtual Device (e.g. `Pixel_7_API_34`) |
| `DEVICE_UDID` | When `TARGET=real_device` | `adb devices` output |
| `DEVICE_NAME` | When `TARGET=real_device` | Human-readable device name |
| `BS_USERNAME` | When `TARGET=browserstack` | BrowserStack account username |
| `BS_ACCESS_KEY` | When `TARGET=browserstack` | BrowserStack access key |
| `BUILD_NAME` | When `TARGET=browserstack` | Build label shown in BrowserStack (default `local`) |
| `ANDROID_HOME` | MCP (`appium-mcp`) | Path to Android SDK root |
| `CAPABILITIES_CONFIG` | MCP (`appium-mcp`) | Path to a capabilities JSON file |
| `GITHUB_PERSONAL_ACCESS_TOKEN` | MCP (`github`) | PAT with repo/issues/PR scopes |

### 3. Start the Appium server

```sh
appium
# Expected: "Appium REST http interface listener started on http://0.0.0.0:4723"
```

---

## Running Tests

```sh
# All tests (default target: emulator)
uv run pytest

# Specific marker
uv run pytest -m smoke
uv run pytest -m regression

# Different target
TARGET=browserstack uv run pytest

# With Allure report generation
uv run pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

Available markers: `smoke`, `regression`, `emulator`, `real_device`, `browserstack`.

---

## Tooling

### pytest
Test runner. Fixtures, markers, and plugins are configured in `pyproject.toml`. Each test gets a fresh driver session (`scope="function"`) to prevent state leakage between tests.

### Appium 3 + UiAutomator2
Drives Android apps over the W3C WebDriver protocol. `UiAutomator2` is Google's on-device automation engine — it understands native Android UI elements without requiring app-source access.

### Allure
Rich HTML reporting (`allure-pytest`). Screenshots captured on test failure are automatically attached to the relevant Allure step. Run `allure serve reports/allure-results` after a test run.

### BrowserStack Automate
Cloud device farm for running tests on real devices without local hardware. Enabled by setting `TARGET=browserstack` and providing credentials in `.env`. Session recordings, network logs, and debug screenshots are enabled automatically.

### Ruff
Fast Python linter and formatter (replaces Flake8 + isort + Black). Configured in `pyproject.toml` with PEP 8 rules, import sorting, and pyupgrade checks.

### uv
High-speed Python package and virtual-environment manager. Resolves and installs the locked dependency graph from `uv.lock` in seconds. Use `uv sync` instead of `pip install -r`.

### python-dotenv
Loads `.env` into `os.environ` at session start. All credentials, paths, and tunable settings live in `.env`; nothing is hardcoded in source.

---

## Framework Architecture

```
conftest.py              # Root: driver fixture, screenshot-on-failure hook
tests/
  conftest.py            # Feature-level fixtures (page objects per feature)
  test_calculator.py     # One test file per feature
pages/
  calculator_page.py     # Page Object per screen
capabilities/
  emulator.py            # build_emulator_caps()
  real_device.py         # build_real_device_caps()
  browserstack.py        # build_browserstack_caps()
utils/                   # Shared helpers (waits, gestures, scroll)
reports/
  allure-results/        # Raw Allure data (gitignored)
  screenshots/           # Failure screenshots (gitignored)
```

### Key design decisions

**Page Object Model** — every screen is a class in `pages/`. Locators are class-level constants using `AppiumBy`; no raw strings. Page methods perform actions and return the next page object on navigation. Assertions never live inside page objects.

**Capability builders** — `capabilities/` contains one builder function per target environment. `conftest.py` selects the right builder via the `TARGET` env var, keeping test code completely target-agnostic.

**Explicit waits only** — `WebDriverWait` + `expected_conditions` everywhere. `time.sleep()` and `driver.implicitly_wait()` are banned. Timeout is read from `WAIT_TIMEOUT` env var.

**Screenshot on failure** — a `pytest_runtest_makereport` hook in `conftest.py` captures a PNG and attaches it to the Allure report automatically; no test-side boilerplate needed.

---

## AI Usage and MCP Servers

AI agents are first-class participants in this project — not just code-completion helpers. The `.mcp.json` file at the repository root wires four MCP servers into your IDE's AI chat.

### What is MCP?
The **Model Context Protocol (MCP)** is an open standard that exposes tools, resources, and actions to AI agents in a structured way. Each MCP server is a small process the agent can call like a function. The IDE starts the servers automatically via `npx`/`docker` when the AI chat is opened.

### Configured MCP servers

| Server | Package | Purpose |
|---|---|---|
| **mobile-mcp** | `@mobilenext/mobile-mcp` | Lets the AI agent interact directly with a running Android app — tap, swipe, read screen content, take screenshots. Used to discover locators and explore app behaviour without manual Appium Inspector sessions. |
| **appium-mcp** | `appium-mcp` | Exposes Appium server controls and device introspection to the agent. Useful for inspecting element trees, sending commands, and verifying session state from inside the chat. |
| **browserstack** | `@browserstack/mcp-server` | Gives the agent access to BrowserStack — upload APKs, list devices, query session results, and retrieve logs — without leaving the IDE. |
| **github** | `ghcr.io/github/github-mcp-server` | Lets the agent read and create issues, open PRs, and check CI status directly from chat. Runs in Docker; needs a PAT in `.env`. |
| **context7** | `@upstash/context7-mcp` | Provides the agent with up-to-date official documentation for any library (Appium, pytest, Allure, Selenium, …). The agent queries context7 before implementing or modifying code so it always uses current API signatures. |

### How AI is used in the workflow

- **Locator discovery** — the agent uses `mobile-mcp` to interact with the live app and identify stable element locators (`resource-id`, `content-desc`), then writes or updates the relevant Page Object.
- **Test generation** — given a feature description and a Page Object, the agent generates `pytest` test functions that follow the project's naming conventions and marker rules.
- **Debugging** — when a test fails, the agent reads the Allure screenshot, queries `appium-mcp` for the current element tree, and suggests a fix.
- **Code quality** — the agent applies the coding rules in `.augment/rules/mobile-testing.md` (explicit waits, no hardcoded timeouts, PEP 8) automatically.
- **CI / issue tracking** — the `github` MCP server lets the agent open a bug ticket or PR from the same chat session that diagnosed the failure.
