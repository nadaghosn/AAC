# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Setup:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the server (from repo root):
```bash
uvicorn app.main:app --reload --port 8000
```

Run all tests:
```bash
pytest tests/ -v
```

Run a single test:
```bash
pytest tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422 -v
```

There is no separate lint/format/build tooling configured in this repo.

The frontend (`frontend/index.html`) is a static, dependency-free HTML/JS file — open it directly in a browser or serve it with any static server (e.g. `python3 -m http.server 5500` from `frontend/`). It calls the API at `http://localhost:8000` (hardcoded `API_BASE` in the `<script>`), so CORS origins in `app/main.py` are tied to whatever port serves it (5500 or 5173 are pre-allowed).

## Architecture

FastAPI app with in-memory storage — no database, no persistence layer. State lives only for the lifetime of the process.

- `app/main.py` — FastAPI app instance, CORS config, and all route handlers (`/tasks` CRUD). Routes are thin: they call into `storage` and `business_rules`, and translate results into HTTP responses/errors.
- `app/models.py` — Pydantic models (`TaskCreate`, `TaskUpdate`, `TaskResponse`) and the `TaskStatus`/`TaskPriority` enums. All models use `extra="forbid"`, so unknown fields in a request body cause a 422. `TaskCreate`/`TaskUpdate` validate `title` (non-blank after strip, ≤200 chars) via `field_validator`.
- `app/storage.py` — the entire persistence layer: a module-level `dict[str, TaskResponse]` (`_tasks`). CRUD functions (`add_task`, `get_all_tasks`, `get_task_by_id`, `update_task`, `delete_task`) operate directly on this dict. `_reset()` clears it and is used by the test fixture between tests — since this is a shared module-level global, tests are not safe to run in parallel without care.
- `app/business_rules.py` — status transition validation. `VALID_TRANSITIONS` is a hardcoded set of allowed `(from, to)` pairs: ToDo→InProgress, InProgress→Done, Done→InProgress. Notably there is no direct ToDo→Done, and setting status to its current value is always invalid (not in the set). Invalid transitions raise `HTTPException(422)` directly from this module (not from a route handler).
- `app/schemas.py` — currently just `HealthResponse`, which is unused: there is no `/health` route wired up in `main.py` despite the README documenting one. If asked to touch health-check behavior, check whether it needs to be added rather than assuming it exists.

Update flow: `update_task` in storage uses `payload.model_dump(exclude_unset=True)` so PATCH is a true partial update — only fields explicitly present in the request body are changed. Status-transition validation happens in `main.py` before calling `storage.update_task`, by comparing the *existing* stored status against the requested new status.

### Tests

`tests/conftest.py` adds the repo root to `sys.path` so `from app...` imports resolve under pytest (there's no package install step). The `_reset_storage` autouse fixture wipes `storage._tasks` before and after every test — tests assume a clean, empty task store.

`tests/verify_a.py` is a standalone manual verification script (not a pytest file — it has no `test_` prefixed functions), run directly with `python tests/verify_a.py` to print PASS/FAIL for a checklist of Pydantic model behaviors.

### Known duplication

A nested `task-tracker-api/` directory exists inside the repo root and currently mirrors `app/`, `frontend/`, `tests/`, and the root config files exactly. It is untracked in git. Don't assume it's stale scaffolding to delete without checking with the user first — confirm which copy is authoritative before editing both or removing either.
