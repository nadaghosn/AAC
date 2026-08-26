# Task Tracker Security Audit

Read-only source audit performed in Codex App.

| ID | Severity | File / location | Finding | Evidence | Suggested next step | Confidence |
|---|---|---|---|---|---|---|
| SEC-01 | Medium | `app/models.py:105-114`, `app/models.py:188-196`, `app/storage.py:15`, `app/main.py:135-163` | Several persisted fields and the task collection are unbounded, creating a memory/response-size exhaustion risk if exposed beyond the course’s local use. | Only `title` has a 200-character limit (`app/models.py:134-139`). `description`, `assignee`, comment text, tag count, and individual tag length have no limits. Tasks accumulate in a module-level dictionary and `GET /tasks` returns all entries without pagination. | Set appropriate field and tag limits, cap collection/list response size with pagination, and add request/rate limits if deployed. | High |
| SEC-02 | Low | `app/models.py:251-263`, `app/storage.py:124-137`, `app/main.py:264-270` | `PATCH` with `{"tags": null}` passes the update schema, then fails during storage re-validation; the route returns `str(exc)` to the client. | `TaskUpdate.tags` is optional and explicitly returns `None`; `TaskResponse.tags` requires a list. The route catches all `ValueError` instances and exposes the raw exception string as the 422 detail. | Reject `null` for update tags in the request model and return a stable, client-safe validation message rather than raw exception text. | High |
| SEC-03 | Low | `app/main.py:38-50` | CORS permits the opaque `"null"` origin and all methods/headers. This allows local-file or sandboxed-origin browser contexts to make cross-origin API requests. | Allowed origins include `"null"`; methods and headers use wildcards. Credentials are disabled, which limits impact, and the other origins are fixed local-development origins. | Remove `"null"` and enumerate only required methods/headers before any non-local use. | High |
| SEC-04 | Medium | `.github/workflows/ci.yml:14-32`, `requirements.txt:1-7` | CI supply-chain integrity is not fully pinned or verified. | GitHub Actions use mutable version tags (`@v4`, `@v5`) rather than commit SHAs. Direct Python dependencies are version-pinned, but installation does not enforce hashes or a fully resolved transitive lock; CI has no dependency-vulnerability scan. | Pin actions by commit SHA, use a hash-locked dependency artifact, and add a dependency/SCA check to CI. | High |
| SEC-05 | Low | `Dockerfile:4`, `Dockerfile:23`, `.dockerignore:1-20` | The container base image uses a mutable tag rather than a digest, so rebuilds can silently receive a different base image. | Both stages use `python:3.11-slim`. The image otherwise has positive controls: multi-stage build, non-root runtime user, and `.env` exclusion from build context. | Pin the Python base image to a reviewed digest and update it through a documented dependency-maintenance process. | High |

## Files inspected

- `../AGENTS.md`
- `app/main.py`, `app/models.py`, `app/schemas.py`, `app/business_rules.py`, `app/storage.py`
- `tests/conftest.py`, `tests/test_tasks.py`, `tests/verify_a.py`
- `requirements.txt`
- `Dockerfile`, `.dockerignore`, `.gitignore`, `.env.example`, `docker-run.sh`
- `../.github/workflows/ci.yml`
- `frontend/index.html`
- `README.md`

## Categories where I found no issue

- Enum handling: status and priority are strict enums; invalid values and unknown request fields are rejected.
- Title validation: trimmed, non-blank, and capped at 200 characters.
- Authorization: absent by explicit course/module decision, documented in `../AGENTS.md` and `README.md`; not reported as a defect for this scope.
- Frontend rendering: task-controlled fields use `textContent`, not HTML insertion.
- Stack traces/debug: no application `debug=True` setting or explicit traceback exposure was visible.
- Secrets: no secret values were found in the reviewed application/deployment configuration; `.env` is ignored and excluded from Docker context.
- Docker privilege: runtime container switches to a non-root user.
- Compose/deployment configuration: no compose file or production hosting configuration was present.

## Assumptions or limits of the audit

- Read-only source review only; I did not run tests, build images, start the API, or perform dependency/CVE scanning.
- The CI workflow is at the parent repository path `../.github/workflows/ci.yml`.
- No `.env` file was inspected, in accordance with repository security instructions.
