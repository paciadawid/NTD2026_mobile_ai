---
type: auto
description: Rules for GitHub Actions CI workflows — env setup, BrowserStack test job, Allure artifact upload, and GitHub Pages publishing. Apply when editing .github/workflows/ files.
---

# GitHub Actions CI Rules

## GitHub Actions
- Always copy `.env.example` to `.env` as the first step after checkout so `python-dotenv` has a base config; job-level `env:` values and secrets override it automatically
- Always upload Allure results as a GitHub Actions artifact after the test step
- Use `if: always()` so results are uploaded even when tests fail
- Name the artifact `allure-results-${{ github.run_number }}` for traceability
- Set `retention-days: 30` to keep results without bloating storage indefinitely
- Use the latest `actions/upload-artifact` (currently `v7`)
- After the test job, run a separate `publish` job that generates the HTML report with `allure generate` and deploys it to GitHub Pages using `actions/deploy-pages`
- Set `if: always()` on the `publish` job so the report is published even when tests fail
- The `publish` job requires `permissions: pages: write` and `id-token: write`

```yaml
- uses: actions/checkout@v6

- name: Copy .env.example to .env
  run: cp .env.example .env

- name: Run tests
  run: uv run pytest tests/ -v --tb=short --alluredir=reports/allure-results

- name: Upload Allure results
  if: always()
  uses: actions/upload-artifact@v7
  with:
    name: allure-results-${{ github.run_number }}
    path: reports/allure-results/
    retention-days: 30
```

```yaml
publish:
  needs: test
  if: always()
  permissions:
    pages: write
    id-token: write
  steps:
    - uses: actions/download-artifact@v8
      with:
        name: allure-results-${{ github.run_number }}
        path: allure-results
    - run: npm install -g allure-commandline
    - run: allure generate allure-results -o allure-report --clean
    - uses: actions/configure-pages@v6
    - uses: actions/upload-pages-artifact@v5
      with:
        path: allure-report
    - uses: actions/deploy-pages@v5
```

To inspect a CI run locally, download the artifact from the GitHub Actions run page and run:
```sh
allure serve <path-to-downloaded-and-unzipped-artifact>
```
