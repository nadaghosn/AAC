# Docker Image — Build & Run (Local)

Ran `docker-run.sh`, which builds the image and starts the container with a health check.

## Result

Built and running successfully — the container reused cached layers from the previous build and passed the healthcheck immediately.

- Image: `task-tracker:dev`
- Container: `task-tracker-dev`, running detached on `localhost:8000`
- `/health` → `{"status":"ok","timestamp":"2026-08-25T10:48:32.253805Z"}`

## Full build/run output

```
==> Building image task-tracker:dev
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 758B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/python:3.11-slim
#2 DONE 1.4s

#3 [internal] load .dockerignore
#3 transferring context: 182B done
#3 DONE 0.0s

#4 [builder 1/5] FROM docker.io/library/python:3.11-slim@sha256:00f89b7f96f13d42900483da3253f8fb2e763eed7a0aa5f0358fec9d15d9f10c
#4 DONE 0.0s

#5 [internal] load build context
#5 transferring context: 660B 0.0s done
#5 DONE 0.0s

#6 [runtime 4/6] COPY --from=builder /opt/venv /opt/venv
#6 CACHED

#7 [builder 2/5] WORKDIR /app
#7 CACHED

#8 [builder 3/5] RUN python -m venv /opt/venv
#8 CACHED

#9 [runtime 5/6] COPY app ./app
#9 CACHED

#10 [runtime 2/6] RUN useradd --uid 1000 --no-create-home --shell /usr/sbin/nologin app
#10 CACHED

#11 [runtime 3/6] WORKDIR /app
#11 CACHED

#12 [builder 5/5] RUN pip install --no-cache-dir -r requirements.txt
#12 CACHED

#13 [builder 4/5] COPY requirements.txt .
#13 CACHED

#14 [runtime 6/6] RUN chown -R app:app /app
#14 CACHED

#15 exporting to image
#15 exporting layers done
#15 writing image sha256:348dab82eac802ec44fa465638f60ce7a0b7c097f9629b6d4553c5a27d98d41b done
#15 naming to docker.io/library/task-tracker:dev done
#15 DONE 0.0s
==> Removing existing container task-tracker-dev
==> Starting container task-tracker-dev on port 8000
5fc4c6b446499383c57d0f6bea4f86ad050a57bc4683a5636b0edba70b0012b3
==> Waiting for /health
==> Healthy:
{"status":"ok","timestamp":"2026-08-25T10:48:32.253805Z"}
```

## Useful follow-up commands

- API base: `http://localhost:8000` (Swagger UI at `/docs`)
- Logs: `docker logs task-tracker-dev`
- Stop/remove: `docker rm -f task-tracker-dev`
