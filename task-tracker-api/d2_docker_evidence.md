# Docker Evidence Summary — `task-tracker-api` (Module 4)

**1) Build command**

The image builds cleanly with `docker build -t task-tracker:dev .`, including a clean `--no-cache` rebuild after the `.dockerignore` fix. The multi-stage Dockerfile installs dependencies into a virtualenv in the `builder` stage, then copies only the populated venv and `app/` source into a fresh `python:3.11-slim` `runtime` stage — no build tools, tests, docs, or `.git` end up in the final image.

**2) Run command**

`docker run -d --name tt-dev -p 8000:8000 task-tracker:dev` starts the container successfully, mapping host port 8000 to the container's port 8000. `docker ps` confirms the container reaches `Up`/`healthy` status, and the process runs via the Dockerfile's exec-form `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]` with no `--reload`.

**3) `/health` check**

`curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health` against the running container consistently returns `HTTP 200`, with body `{"status":"ok","timestamp":"..."}`. This matches the Dockerfile's own `HEALTHCHECK` directive, which polls the same endpoint every 30 seconds using Python's stdlib `urllib.request` (no `curl` baked into the image).

**4) Non-root check — implemented**

The runtime stage creates a dedicated `app` user (`useradd --uid 1000 --no-create-home --shell /usr/sbin/nologin app`) and switches to it via `USER app` before `EXPOSE`, `HEALTHCHECK`, and `CMD`. Verified live: `docker exec tt-dev whoami` and `docker inspect --format='{{.Config.User}}' tt-dev` both return `app`, confirming the container process never runs as root.

**5) No-baked-secrets check**

The Dockerfile copies only `requirements.txt` and `app/` — no wildcard `COPY . .` and no reference to `.env` or secret files anywhere in the build. `.dockerignore` excludes `.env`, `.env.*`, `.git`, `venv/`, `.venv/`, and (after fixing a nested-path gap with `**/`-prefixed patterns) `__pycache__`/`.pyc` at any depth. A `find /app -iname '.env*' -o -iname '.git' -o -iname 'venv' -o -iname '__pycache__'` run inside the built image returns empty, confirming no secrets, VCS metadata, or stale caches leak into the runtime image.
