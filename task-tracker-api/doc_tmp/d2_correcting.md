# Module 4 — D2 Correcting: .dockerignore Pycache Leak

Summary of the issue found during D2 verification, the fix, and the commit/push that closed it out.

## What was found

Running the D2 verification commands (see `d2.md`) against `task-tracker:dev` / `tt-dev`, 5 of 6 checks passed. Check 5 — "`.dockerignore` excludes `.env`, `.git`, virtual environments, and caches" — partially failed:

```bash
docker run --rm task-tracker:dev sh -c "find /app -iname '.env*' -o -iname '.git' -o -iname 'venv' -o -iname '.venv' -o -iname '__pycache__'"
```
returned `/app/app/__pycache__` instead of empty output, even after a `--no-cache` rebuild.

## Root cause

Docker's `.dockerignore` matching is **not** gitignore-style recursive by default. A bare pattern like `__pycache__/` only matches at the **root** of the build context, not nested paths such as `app/__pycache__`. The local `app/` directory had a `__pycache__` left over from running `pytest` on the host, and it was being copied into the image despite the exclusion rule appearing to be present.

## Fix applied

Added `**/`-prefixed variants to `.dockerignore` so the patterns match at any depth:

```diff
 venv/
 .venv/
 __pycache__/
+**/__pycache__/
 *.pyc
+**/*.pyc
 *.pyo
+**/*.pyo
```

## Verification after the fix

1. Rebuilt with `docker build --no-cache -t task-tracker:dev .` — succeeded.
2. `find /app -iname '.env*' -o -iname '.git' -o -iname 'venv' -o -iname '.venv' -o -iname '__pycache__' -o -iname '*.pyc'` inside the rebuilt image → **empty output (pass)**.
3. Re-ran the full D2 check set against a fresh `tt-dev` container: container up on `0.0.0.0:8000->8000/tcp`, `/health` → `HTTP 200`, `docker exec tt-dev whoami` → `app`, both build stages still pinned to `python:3.11-slim`, no secrets/wildcard `COPY . .` in the Dockerfile.

Full details and command-by-command output saved in `d2_test.md`.

## Commit / push

Staged and committed the fix along with the session's D1/D2 documentation and `docker-run.sh`:

```bash
git add .dockerignore docker-run.sh d1.md d1_healthcheck.md d1_tables.md d1_test.md d2.md d2_test.md docker_image.md docker_container_200.md dockerdaemon.md
git commit -m "Add Module 4 Docker verification docs and fix .dockerignore pycache leak"
git push origin final-project
```

Result: commit `40474ff` pushed to `origin/final-project` (`3bf6057..40474ff`). Working tree clean, branch up to date with remote.

## Status

All 6 D2 checks pass. `.dockerignore` fix is committed and pushed — no further action needed on this issue.
