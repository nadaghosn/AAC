# Docker Container — /health Returns HTTP 200

Verified the running `task-tracker-dev` container responds to `GET /health` with HTTP 200.

## Commands

```bash
curl -s -o /dev/null -w "HTTP status: %{http_code}\n" http://localhost:8000/health
curl -s http://localhost:8000/health
```

## Output

```
HTTP status: 200
---body---
{"status":"ok","timestamp":"2026-08-25T10:50:06.708513Z"}
```

## Result

Confirmed: `GET /health` returns **HTTP 200** with body `{"status":"ok","timestamp":"2026-08-25T10:50:06.708513Z"}`.
