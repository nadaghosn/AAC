# Release Evidence — CI Evidence

**1) Workflow file:** `.github/workflows/ci.yml` (lives at the outer repository root — `../.github/workflows/ci.yml` relative to `task-tracker-api/`, not inside this module; `defaults.run.working-directory: task-tracker-api` scopes its steps here)

**2) Latest run link:** [`https://github.com/nadaghosn/AAC/actions/runs/32868169333`](https://github.com/nadaghosn/AAC/actions/runs/32868169333) — **SUCCESS**, branch `final-project`, triggered by push (commit `b0c7ba9`, 2026-08-25). Pulled live via `gh run list`/`gh run view`, not from an older cached note.

**3) Test command used by CI:**
```yaml
run: pytest -v --tb=short
```
(from `ci.yml`'s "Run tests" step, after `pip install -r requirements.txt`)

**4) Shortcut check:**

| Check | Status |
|---|---|
| `continue-on-error` | ✅ Not present anywhere in the workflow |
| `\|\| true` (or similar exit-code-swallowing) | ✅ Not present — no `\|\|`, `\|`, or `tee` on any `run:` line |
| `pytest` step skipped | ✅ Not skipped — runs unconditionally, no `if:` guard |

(Full detail in `b1_dangerous.md`.)

## Note

The latest run's log includes one informational annotation — `Node.js 20 is deprecated... actions/cache@v4, actions/checkout@v4, actions/setup-python@v5` will be forced onto Node 24 by GitHub. Not a failure, not one of the 4 requested checks, but flagged since it's a real live-run observation, not invented.
