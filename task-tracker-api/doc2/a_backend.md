# API Startup + Health Check

**Command used to start the API:**
```bash
uvicorn app.main:app --port 8000
```

**Result of `GET /health`:**
```
HTTP 200
{"status":"ok","timestamp":"2026-08-25T16:00:37.555089Z"}
```

Confirmed against a freshly started local `uvicorn` process (not a cached/in-process client) — no code changed.
