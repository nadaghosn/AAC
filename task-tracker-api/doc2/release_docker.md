# Release Evidence — Docker Evidence

**1) Build command:**
```bash
docker build -t task-tracker:dev .
```
Result: build succeeded, image `task-tracker:dev` created (`sha256:367c976583f5...`).

**2) Run command:**
```bash
docker run -d --name task-tracker-dev -p 8000:8000 task-tracker:dev
```
Result: container up, `0.0.0.0:8000->8000/tcp`.

**3) `/health` check:**
```
HTTP 200
{"status":"ok","timestamp":"2026-08-25T16:17:43.577639Z"}
```

**4) Non-root check — implemented:**
```bash
docker exec task-tracker-dev whoami        # → app
docker inspect --format='{{.Config.User}}' task-tracker-dev   # → app
```
Confirmed: the container runs as the dedicated `app` user (uid 1000), not root.

**5) No-baked-secrets check:**
```bash
docker run --rm task-tracker:dev sh -c "find /app -iname '.env*' -o -iname '.git' -o -iname 'venv' -o -iname '.venv' -o -iname '__pycache__' -o -iname '*.pyc'"
```
Result: empty output — no `.env`, `.git`, virtualenv, or cache files present in the built image.
