# Module 4 — D2 Test: .dockerignore Fix + Verification Run

Fixed the `__pycache__` leak found in the D2 verification (see `d2.md`) and re-ran all checks against `task-tracker:dev` / `tt-dev`.

## Root cause

Docker's `.dockerignore` matching is not gitignore-style recursive by default — a bare pattern like `__pycache__/` only matches at the **root** of the build context, not nested paths like `app/__pycache__`. The local `app/` directory had a `__pycache__` from running pytest on the host, and it was getting copied into the image despite the exclusion rule being present.

## Fix applied to `.dockerignore`

Added `**/`-prefixed variants so the patterns match at any depth:

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

Full updated `.dockerignore`:

```
.git
.github
.gitignore
.env
.env.*
venv/
.venv/
__pycache__/
**/__pycache__/
*.pyc
**/*.pyc
*.pyo
**/*.pyo
.pytest_cache/
.coverage
htmlcov/
tests/
docs/
.claude/
CLAUDE.md
```

## Rebuild (--no-cache) to confirm the fix

```bash
docker build --no-cache -t task-tracker:dev .
```

Result: build succeeded, `naming to docker.io/library/task-tracker:dev done`.

## Verification results (post-fix)

| Check | Command | Result |
|---|---|---|
| No leaked `__pycache__`/`.pyc`/etc. in image | `docker run --rm task-tracker:dev sh -c "find /app -iname '.env*' -o -iname '.git' -o -iname 'venv' -o -iname '.venv' -o -iname '__pycache__' -o -iname '*.pyc'"` | **empty output — pass** |
| Container starts on port 8000 | `docker run -d --name tt-dev -p 8000:8000 task-tracker:dev` | `tt-dev` `Up`, `0.0.0.0:8000->8000/tcp` |
| `GET /health` | `curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8000/health` | `HTTP 200`, body `{"status":"ok","timestamp":"2026-08-25T11:01:23.521783Z"}` |
| Non-root user | `docker exec tt-dev whoami` / `docker inspect --format='{{.Config.User}}' tt-dev` | `app` / `app` |
| Base image / no secrets | `grep -n '^FROM' Dockerfile` / `grep -inE '\.env\|secret\|COPY \. \.' Dockerfile` | Both stages `python:3.11-slim`; no secret/wildcard-copy matches |

## Security log

```
[non-root]         container runs as uid=1000 user=app (verified: docker exec tt-dev whoami → app)
[slim base]        both stages pinned python:3.11-slim, no :latest (verified: grep '^FROM' Dockerfile)
[no baked secrets] no .env/.git/secret/__pycache__ files found in image after .dockerignore fix (verified: find /app inside image → empty)
```

## Status

All 6 D2 checks now pass. `.dockerignore` fix applied but not yet committed.
