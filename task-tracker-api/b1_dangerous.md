# CI Dangerous-Shortcuts Check — `.github/workflows/ci.yml`

Checked `.github/workflows/ci.yml` directly (fresh read of the actual file, not from older review docs) for common CI shortcuts that mask real failures.

## Checks

| # | Check | Status | Evidence |
|---|---|---|---|
| 1 | `continue-on-error` | ✅ Not present | Full file grep — no `continue-on-error` key anywhere in the job or any step |
| 2 | `\|\| true` (or similar exit-code-swallowing) | ✅ Not present | No `\|\|`, `\|`, `tee`, or subshell wrapping on any `run:` line |
| 3 | Skipped pytest command | ✅ Not skipped | `Run tests` step (line 34-35) runs `pytest -v --tb=short` directly — no `if:` condition disabling it, not commented out |
| 4 | Vague Python version | ✅ Explicit | `python-version: "3.11"` (line 20) — pinned to the exact minor version required by `CLAUDE.md` ("Python 3.11 at least"), not a wildcard like `"3.x"` or `"*"` |
| 5 | Missing dependency installation | ✅ Present | `Install dependencies` step (line 31-32) runs `pip install -r requirements.txt` before tests run |

## Conclusion

No issues found. The workflow is a straightforward 5-step pipeline: checkout → set up Python 3.11 → cache pip → upgrade pip → install deps → run `pytest -v --tb=short`, with nothing masking a real test failure.

## Full file content (for reference)

```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: task-tracker-api
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('task-tracker-api/requirements.txt') }}

      - name: Upgrade pip
        run: python -m pip install --upgrade pip

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest -v --tb=short
```
