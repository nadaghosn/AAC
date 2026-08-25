# Dockerfile HEALTHCHECK — Verification Run

## Commands run

```bash
docker build -t task-tracker-api:healthcheck-test .
docker run -d --name tta-healthcheck-test -p 18000:8000 task-tracker-api:healthcheck-test
docker inspect --format='{{.State.Health.Status}}' tta-healthcheck-test
docker exec tta-healthcheck-test whoami
docker inspect --format='{{json .State.Health}}' tta-healthcheck-test
curl -s http://127.0.0.1:18000/health
docker exec -u 0 tta-healthcheck-test cat /etc/passwd | grep app
docker exec -u 0 tta-healthcheck-test sh -c 'ls -la /home/; ls -ld /home/app'
docker rm -f tta-healthcheck-test
docker rmi task-tracker-api:healthcheck-test
```

## Results

**Build:** succeeded, all layers completed (`exited with code 0`), dependencies installed into `/opt/venv` in the builder stage as expected.

**Container startup — health status transitions:**
- Immediately after `docker run`: `starting`
- After the first `HEALTHCHECK` cycle completed: `healthy`

**Health log entry (via `docker inspect .State.Health`):**
```json
{
    "Status": "healthy",
    "FailingStreak": 0,
    "Log": [
        {
            "Start": "2026-08-25T13:14:06.048Z",
            "End": "2026-08-25T13:14:06.659Z",
            "ExitCode": 0,
            "Output": ""
        }
    ]
}
```
Exit code `0`, empty output — confirms the `urllib.request.urlopen(...)` call against `http://127.0.0.1:8000/health` succeeded inside the container with no unhandled exception, in ~0.6s (well under the 5s timeout).

**Direct `/health` check via the published port:**
```
GET http://127.0.0.1:18000/health
{"status":"ok","timestamp":"2026-08-25T10:14:20.681949Z"}
```
Confirms the app itself is reachable and returning the expected `HealthResponse` shape from outside the container too, not just from the healthcheck's internal loopback call.

**Non-root user verification:**
- `docker exec ... whoami` → `app` (process runs as the non-root `app` user, not root)
- `/etc/passwd` entry: `app:x:1000:1000::/home/app:/usr/sbin/nologin` — UID 1000 as required, `nologin` shell as designed
- `/home/app` does **not** actually exist on disk (`ls: cannot access '/home/app': No such file or directory`) — confirms `--no-create-home` worked; the `/home/app` string in `/etc/passwd` is just the default home-field metadata `useradd` assigns, not an actual created directory
- `ps` is not available in the image (expected — `python:3.11-slim` doesn't ship `procps`; not needed for this app to function)

## Cleanup

Test container and image were removed after verification (`docker rm -f`, `docker rmi`) — no test artifacts left running or cached.

## Conclusion

The `HEALTHCHECK` instruction works as designed: it correctly reports `starting` → `healthy`, the underlying `/health` endpoint responds correctly, and the container runs entirely as the non-root `app` user (UID 1000, no home directory, `nologin` shell) as required.
