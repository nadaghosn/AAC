# Release Evidence — Baseline

**1) Branch:** `final-project`

**2) Date:** 2026-08-25

**3) Local app run command:**
```bash
uvicorn app.main:app --reload --port 8000
```

**4) `/health` result:**
```
HTTP 200
{"status":"ok","timestamp":"2026-08-25T16:04:15.280218Z"}
```

**5) Frontend check:** `frontend/index.html` (served via `python -m http.server 5500` from `frontend/`) — the three-column Kanban board (`To Do`, `In Progress`, `Done`) and the create/edit task flow (`New Task` button, `#task-modal` with `Edit Task` mode) are present and intact in the markup/JS.

**6) Test command:**
```bash
pytest -v
```

**7) Test result:**
```
45 passed in 0.74s
```
