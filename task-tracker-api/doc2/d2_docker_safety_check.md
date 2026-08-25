# Docker Safety Check — `task-tracker-api` (Module 4)

**1) Non-root user — implemented**

`Dockerfile:15` creates a dedicated user (`useradd --uid 1000 --no-create-home --shell /usr/sbin/nologin app`), and `Dockerfile:26` switches to it with `USER app` before `EXPOSE`/`HEALTHCHECK`/`CMD` — so the app process never runs as root.

Verified live: `docker exec tt-dev whoami` → `app`; `docker inspect --format='{{.Config.User}}' tt-dev` → `app`.

**2) No `.env`/secrets copied — implemented**

Dockerfile only copies `requirements.txt` and `app/` (`Dockerfile:9,20`) — no wildcard `COPY . .`, no `.env` or secret references anywhere in the file. `.dockerignore` explicitly excludes `.env`, `.env.*`, `.git`, `venv/`, `.venv/`, and (after the fix in `d2_correcting.md`) `__pycache__`/`.pyc` at any depth.

Verified live: `find /app -iname '.env*' -o -iname '.git' -o -iname 'venv' -o -iname '.venv' -o -iname '__pycache__'` inside the built image → empty.

**3) Clear runtime command — implemented**

`Dockerfile:32`: `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]` — exec form, no shell wrapper, no `--reload` (dev-only flag correctly omitted for the image). Paired with `HEALTHCHECK` (`Dockerfile:30`) hitting `/health` every 30s.
