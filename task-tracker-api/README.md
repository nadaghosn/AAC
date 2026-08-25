# Task Tracker API (Module 4)

A learning-project REST API for tracking tasks and their comments, built with Python, FastAPI, and Pydantic. Storage is in-memory only; the API supports full task CRUD, tag/status/priority filtering, status-transition rules, and a single comment per task. Module 4 adds a Dockerfile and CI workflow on top of the Module 1–3 application.

This is a learning project. It is **not** deployment-ready: there is no authentication/authorization, no database or persistent storage, and no production process manager or hosting configuration (see [Limitations](#project-conventions-and-current-limitations) below).

## Prerequisites

- Python 3.11+
- `pip` and the standard library `venv` module
- Docker (only needed for the [Run with Docker](#run-with-docker) section)

## Local setup

All commands below assume your working directory is `task-tracker-api/` (this directory). The actual git repository root is one level up, at the parent `AAC/` folder — confirm this README should treat `task-tracker-api/` as the effective project root.

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

An `.env.example` file is provided (`PORT`, `APP_ENV`). Copying it to `.env` is optional — `python-dotenv` loads it at startup, but neither variable currently changes runtime behavior (`PORT` isn't read anywhere in `app/`, and `APP_ENV` is assigned once in `app/main.py` but not used afterward).

## Run the app locally

```bash
uvicorn app.main:app --reload --port 8000
```

- API base: `http://localhost:8000`
- Interactive docs (Swagger UI): `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

To also run the static frontend (a single `index.html`, no build step):
```bash
cd frontend
python -m http.server 5500
```
Then open `http://localhost:5500`. (CORS is configured in `app/main.py` to allow this origin — see `app/main.py`'s `CORSMiddleware` config if you serve the frontend from elsewhere.)

## Run tests

```bash
pytest -v
```

This discovers the full suite under `tests/` (currently 45 tests in `tests/test_tasks.py`, covering task CRUD, tags, comments, and status transitions).

`tests/verify_a.py` is a separate, standalone manual verification script (not part of the pytest suite — it has no `test_`-prefixed functions) and is run directly:
```bash
python tests/verify_a.py
```

## Run with Docker

Build and run manually:
```bash
docker build -t task-tracker:dev .
docker run -d --name task-tracker-dev -p 8000:8000 task-tracker:dev
curl http://localhost:8000/health
```

Or use the included convenience script, which builds the image, (re)starts the container, and polls `/health` until it reports healthy:
```bash
./docker-run.sh
```

Notes on the image (`Dockerfile`):
- Multi-stage build (`builder` installs dependencies into a virtualenv; `runtime` copies only the populated venv and `app/` source — no build tools, tests, or `.git` in the final image).
- Runs as a non-root user (`app`, uid 1000), not root.
- `HEALTHCHECK` polls `/health` every 30s using Python's stdlib `urllib` (no extra HTTP client installed).
- No `--reload` in the container's `CMD` — this is a static runtime image, not a dev server.

To stop and remove the container:
```bash
docker rm -f task-tracker-dev
```

## CI workflow summary

The workflow file lives outside this directory, at `../.github/workflows/ci.yml` relative to `task-tracker-api/` — i.e., at the outer repository's root, not inside this module.

- **Triggers:** every `push` and every `pull_request` (no branch filters).
- **Job:** runs on `ubuntu-latest` with `working-directory: task-tracker-api` for all steps.
- **Steps:** checkout (`actions/checkout@v4`) → set up Python 3.11 (`actions/setup-python@v5`) → cache `~/.cache/pip` (keyed on the hash of `task-tracker-api/requirements.txt`) → `pip install --upgrade pip` → `pip install -r requirements.txt` → `pytest -v --tb=short`.
- **What it does not do:** it does not build or run the Docker image, and it does not deploy anywhere — it only installs dependencies and runs the pytest suite.

## Project structure

```
task-tracker-api/
├── app/
│   ├── main.py            # FastAPI app instance, CORS config, all route handlers
│   ├── models.py          # Pydantic request/response models and field validation
│   ├── storage.py         # In-memory persistence (module-level dict)
│   ├── business_rules.py  # Task status transition rules
│   └── schemas.py         # HealthResponse, used by GET /health
├── frontend/
│   └── index.html         # Single-file board UI (To Do / In Progress / Done), no build step
├── tests/
│   ├── conftest.py        # Shared fixtures (client, created_task) and storage-reset fixture
│   ├── test_tasks.py      # pytest suite (44 tests)
│   └── verify_a.py        # Standalone manual verification script (not pytest)
├── docs/midcourse/        # Course deliverables: user stories, mini-ADR, verification, reflection
├── Dockerfile              # Multi-stage build, non-root user, HEALTHCHECK
├── .dockerignore
├── docker-run.sh           # Build + run + healthcheck convenience script
├── requirements.txt
└── README.md
```

The repository root also contains several dated markdown notes from course modules (design drafts, verification logs, CI proof checklists) that document the process behind this work but aren't part of the running application.

## Project conventions and current limitations

- **Storage is in-memory only.** Data resets whenever the process restarts; there is no database and none is planned for this module (per project constraints).
- **No authentication or authorization.** Every endpoint is open.
- **CORS is restricted** to a fixed list of local dev origins (`localhost:5500`, `127.0.0.1:5500`, `localhost:5173`, and `"null"`) — see `app/main.py`. Update this list if you serve the frontend from elsewhere.
- **A task holds at most one comment**, enforced in `app/storage.py`.
- **Status transitions are restricted**: `ToDo → InProgress`, `InProgress → Done`, `Done → InProgress`, and each status to itself; any other transition returns `422` (see `app/business_rules.py`).
- **`title` is required and non-blank** (after stripping) on both create and update, max 200 characters; `tags` are normalized (lowercased, stripped, de-duplicated); `comment` is optional and normalized similarly.
- **PATCH and PUT on `/tasks/{task_id}/comments` currently behave identically** — both fully overwrite the comment's text and preserve its original timestamp. If distinct partial-vs-full-replace semantics were intended, they aren't implemented yet.
- **`pydantic-settings` is an unused dependency** — pinned in `requirements.txt` but not referenced anywhere in `app/` or `tests/`.
- **`data/tasks.json`** is present in the repo but not read or written by any application code yet.
- **Not deployment-ready.** The Dockerfile and CI workflow added in this module support local/dev verification (build, healthcheck, automated test runs) — they do not constitute a deployment pipeline, and no hosting, database, or auth has been added.

## Technical notes / decisions

No `docs/decisions/` directory exists in this repository. The closest available technical note is the mini-ADR from the course midcourse deliverables, covering the storage and tags decisions:
- [`docs/midcourse/mini-adr.md`](docs/midcourse/mini-adr.md)

Other related course documentation lives alongside it in [`docs/midcourse/`](docs/midcourse/) (user stories, verification notes, reflection).
