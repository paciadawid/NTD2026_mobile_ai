# Workshop Setup — AI-Powered E2E Mobile Testing With Appium And Mobile MCP

> Hi! Below are the steps to prepare your machine **before** the workshop. Mobile E2E setup is a bit more involved than web — please allocate ~60–90 minutes the day before, plan for **~10–12 GB of downloads + disk space** (Android Studio + one system image alone is ~8 GB), and use a stable internet connection. In ~90% of cases it goes smoothly. If you get stuck, ping me on LinkedIn (https://www.linkedin.com/in/paciadawid/) or email **paciadawid@gmail.com** — ideally by **EOD June 2** so we have time to fix things before the session.
>
> Works on **Windows, macOS, and Linux**. We'll only target **Android** (saves us from the Xcode/iOS rabbit hole).
>
> **On a corporate laptop?** `npm i -g appium`, Android SDK Manager downloads, and AI-plugin sign-in are the three things most likely to be blocked by proxies/firewalls. Please check with IT in advance.

---

## TL;DR — What you'll install

1. **Python 3.14** (or 3.13) and **PyCharm** (latest, free tier)
2. **Node.js 24 LTS**
3. **Java JDK 25** (current LTS, with `JAVA_HOME`)
4. **Android Studio** (latest) + emulator with **Android 16 / API 36** (with `ANDROID_HOME`)
5. **Appium 3** (latest) + **UiAutomator2** driver (latest)
6. **Appium Inspector** (latest)
7. **AI plugin for PyCharm** — **GitHub Copilot** (recommended) or any other AI assistant you already use

> **Mobile MCP** ([mobile-next/mobile-mcp](https://github.com/mobile-next/mobile-mcp) — an MCP server that lets AI tools drive Android/iOS apps) does **not** need to be installed upfront — we'll wire it into your IDE together during the workshop. Just make sure Node.js (step 2) is installed (Mobile MCP runs via `npx`) and your AI plugin (step 7) supports MCP.

A short validation checklist is at the very end. **Please run it before the workshop.**

> **The app under test:** I'll share a sample Android app on the day. You don't need to download or build any APK in advance.

---

## 1. Python + PyCharm

1. Install **Python 3.14** (current stable; 3.13 also works) → https://www.python.org/downloads
   - **Windows:** tick **"Add Python to PATH"** in the installer.
2. Verify in a fresh terminal:
   ```
   python --version    # expected: 3.13 or 3.14 (try python3 if python isn't found)
   pip --version
   ```
   If `python` is not recognized on Windows, follow → https://realpython.com/add-python-to-path/
3. Install **PyCharm** (latest) → https://www.jetbrains.com/pycharm/download
   - PyCharm is now a **single unified product** with a free tier — no separate "Community Edition" anymore. At first launch, choose **"Use PyCharm for free"** when prompted. A JetBrains account is **not required** for the free tier (only for Pro/trial).

---

## 2. Node.js

We need Node for Appium and (later) for the Mobile MCP server.

1. Install **Node.js 24 LTS** → https://nodejs.org/en (pick the "LTS" button).
2. Verify:
   ```
   node --version    # v24.x expected
   npm --version
   ```
   (`npx` ships with `npm`, no separate check needed.)

---

## 3. Java JDK 25 (LTS)

1. Install **JDK 25 LTS** — Temurin/Adoptium is the easiest → https://adoptium.net/temurin/releases/?version=25 (or Oracle: https://www.oracle.com/java/technologies/downloads/). On the Adoptium page, make sure **Version** is set to **25 - LTS** before downloading.
2. Set `JAVA_HOME` and add `$JAVA_HOME/bin` (Windows: `%JAVA_HOME%\bin`) to `PATH`. Guide → https://www.baeldung.com/java-home-on-windows-mac-os-x-linux
3. Verify in a **new** terminal:
   ```
   java -version             # 25.x
   echo $JAVA_HOME           # macOS/Linux
   echo %JAVA_HOME%          # Windows (cmd)
   $env:JAVA_HOME            # Windows (PowerShell)
   ```

**Common pitfalls**
- After setting env vars on Windows, **close and reopen** the terminal (and PyCharm).
- On macOS with multiple JDKs: `/usr/libexec/java_home -V` lists installed ones.
- Don't worry about Android Studio — it bundles its own JDK internally and ignores your `JAVA_HOME`. The system JDK we install here is what **Appium** uses from the command line.

---

## 4. Android Studio + Emulator + `ANDROID_HOME`

1. Install the **latest Android Studio** → https://developer.android.com/studio (choose **Standard** install).
2. Open **SDK Manager** → install **Android 16 (API 36)**.
3. Open **Device Manager** → **Create device** → **Pixel 6** or **Pixel 8** → pick the **API 36** image → **Finish**.
4. **Start the emulator at least once** and confirm it **boots all the way to the home screen**. (This is the single most common point of failure — please don't skip it.)
5. Set `ANDROID_HOME` (or `ANDROID_SDK_ROOT`) to your SDK path:
   - macOS default: `~/Library/Android/sdk`
   - Windows default: `%LOCALAPPDATA%\Android\Sdk`
   - Linux default: `~/Android/Sdk`

   Also add to `PATH`:
   - **macOS/Linux:** `$ANDROID_HOME/platform-tools`, `$ANDROID_HOME/emulator`, `$ANDROID_HOME/cmdline-tools/latest/bin`
   - **Windows:** `%ANDROID_HOME%\platform-tools`, `%ANDROID_HOME%\emulator`, `%ANDROID_HOME%\cmdline-tools\latest\bin`

   Step-by-step → https://www.dev2qa.com/how-to-set-android-sdk-path-in-windows-and-mac/
6. Verify in a **new** terminal (an AVD = Android Virtual Device = an emulator instance):
   ```
   echo $ANDROID_HOME        # macOS/Linux
   echo %ANDROID_HOME%       # Windows (cmd)
   $env:ANDROID_HOME         # Windows (PowerShell)
   adb --version             # works
   emulator -list-avds       # should print the name of the emulator you created
   ```

**Common pitfalls**
- Apple Silicon Macs: use **arm64** system images, not x86_64.
- Windows: if `adb` not found, your `PATH` is missing `platform-tools`.
- If `emulator` is not found, your `PATH` is missing the `emulator` directory.
- If the emulator is super slow on Windows, enable virtualization in BIOS / Hyper-V.

---

## 5. Appium 3 + UiAutomator2 driver

1. Install the latest **Appium 3** globally:
   ```
   npm i -g appium@latest
   appium --version          # 3.x
   ```
   *(If `appium@latest` ever resolves to 2.x on your machine, try `npm cache verify` first; if it still resolves to 2.x, force it: `npm i -g appium@3`.)*

   **macOS/Linux:** if you get an `EACCES` permission error, **set up a user-level npm prefix** (recommended) → https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally. `sudo npm i -g …` also works as a last resort but isn't recommended.
2. Install the latest Android driver:
   ```
   appium driver install uiautomator2
   appium driver list --installed
   ```
3. Run Appium's built-in environment check:
   ```
   appium driver doctor uiautomator2
   ```
   Everything should be green ✅. If not, fix the reported items (usually `JAVA_HOME` or `ANDROID_HOME`).
4. Smoke-test Appium server (leave it running for a few seconds, then `Ctrl+C`):
   ```
   appium
   ```
   You should see `Appium REST http interface listener started on http://0.0.0.0:4723`.

**Note:** Appium 3 requires Node `^20.19.0 || ^22.12.0 || >=24.0.0` and `npm >= 10` — the Node 24 LTS from step 2 covers both. If you're on an older Node (18, early 20.x), upgrade before installing Appium.

---

## 6. Appium Inspector

Download the **latest** release → https://github.com/appium/appium-inspector/releases (pick the asset for your OS).

We'll use it during the workshop to compare "classic" element inspection vs. AI-driven discovery.

---

## 7. AI plugin for PyCharm — pick ONE

We'll use AI to drive Mobile MCP — either through a PyCharm plugin or a separate AI tool that runs alongside PyCharm. Pick one of the options below. **Do not configure Mobile MCP yet** — we'll do that together.

### Option A (recommended) — GitHub Copilot

> Heads-up: GitHub paused new sign-ups for **Copilot Pro / Pro+ / Student** in late April 2026. **Copilot Free** is open for new accounts. Paid sign-ups reopen **June 1, 2026** under a new usage-based (AI Credits) billing model — if you're reading this after June 1, Pro is available again.
>
> ⚠️ **Copilot Free is limited**: only a small subset of models is available (e.g. Haiku 4.5, GPT-5 mini), with **~50 agent/chat requests per month** and **~2,000 code completions per month**. That's enough to get a feel for the workshop, but you'll likely hit the cap if you experiment heavily. If you can, upgrade to **Pro** for more requests and access to stronger models.

1. Sign in / create a **GitHub account** → https://github.com.
2. Enable **Copilot Free** → https://github.com/features/copilot (click **"Get started"** and follow the Free flow).
3. In PyCharm: **Settings → Plugins → Marketplace → "GitHub Copilot" → Install → Restart**.
4. Sign in via the **Copilot icon in the status bar** (bottom-right) — or **Tools → GitHub Copilot → Login to GitHub** in older plugin versions.
5. Open the **Copilot Chat** tool window and confirm chat works (e.g. ask *"Say hello"*).

### Option B — Any other AI assistant you already use

If you already have a paid/working setup with another AI tool that **supports MCP servers** — feel free to use it. Confirmed MCP-capable tools include **JetBrains AI Assistant** (recent versions), **Cursor**, **Windsurf** (Cascade), **Tabnine** (5.26+), **Cline**, and **Continue**. **Claude Code** also supports MCP, but it runs as a terminal CLI alongside PyCharm rather than as a PyCharm plugin — the integration model is different but works fine for the workshop. Always double-check your tool's current docs, as MCP support has been moving fast.

Just make sure **before the workshop**:

1. The plugin/extension is **installed in PyCharm** (or runs alongside it).
2. You're **logged in** and chat / inline completions work.
3. You know where MCP servers are configured in its settings — we'll wire Mobile MCP in during the workshop.

> Stick to one tool — installing multiple AI plugins side-by-side often causes keymap conflicts and confusing completions.

---

## 8. PyCharm project warmup

So PyCharm + the Appium client are ready to go:

1. Create a new PyCharm project with a fresh virtual environment (Python 3.14, or 3.13).
2. In the PyCharm terminal:
   ```
   pip install --upgrade pip
   pip install Appium-Python-Client pytest
   ```
3. Verify:
   ```
   python -c "from appium import webdriver; print('ok')"
   pytest --version
   ```

We'll write the actual test code together during the workshop — no need to prepare more than this.

---

## ✅ Final pre-workshop checklist

Run each of these in a **new** terminal. All must succeed:

```
python --version                  # 3.13 or 3.14
node --version                    # v24.x
java -version                     # 25.x
echo $JAVA_HOME                   # macOS/Linux  (Windows cmd: echo %JAVA_HOME%  ·  PowerShell: $env:JAVA_HOME)
echo $ANDROID_HOME                # macOS/Linux  (Windows cmd: echo %ANDROID_HOME%  ·  PowerShell: $env:ANDROID_HOME)
adb --version                     # works
emulator -list-avds               # shows the emulator you created
appium --version                  # 3.x
appium driver list --installed    # uiautomator2 listed
python -c "from appium import webdriver; print('ok')"   # prints: ok
pytest --version                  # works
```

Plus:
- [ ] Android emulator (the AVD you created, API 36) starts and **boots all the way to the home screen**.
- [ ] `appium driver doctor uiautomator2` is fully green.
- [ ] Appium Inspector opens.
- [ ] PyCharm is installed (free tier active).
- [ ] GitHub Copilot (or your preferred AI assistant) is installed in PyCharm, signed in, and chat works.

If **all** boxes are ticked — you're ready. 🎉

See you at the workshop!

— Dawid
