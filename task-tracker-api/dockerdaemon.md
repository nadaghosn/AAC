# Docker Daemon

The Docker daemon (`dockerd`) is the background service that does all the actual work — the `docker` command you type is just a CLI client that talks to it.

## How it fits together

- **`docker` CLI** — the client. Parses your command (`docker build`, `docker run`, etc.) and sends it as an API request to the daemon.
- **`dockerd`** — the daemon. Runs continuously in the background (on Linux, usually as a systemd service; on Mac/Windows, inside Docker Desktop's VM). It does the real work: builds images, manages containers, handles networking, stores/manages layers and volumes.
- They talk over a Unix socket (`/var/run/docker.sock` on Linux) or occasionally a TCP socket if configured remotely.

## Why it matters for `docker-run.sh`

- `docker build -t task-tracker:dev .` — your CLI sends the Dockerfile + build context to the daemon; the daemon executes each instruction (`FROM`, `RUN`, `COPY`, etc.) as its own layer and caches them.
- `docker run -d ...` — the daemon creates and starts the container process, using the kernel's namespaces/cgroups for isolation, and keeps it running even after your terminal session ends (that's what `-d`/detached does).
- `docker ps`, `docker logs`, `docker rm` — all just queries/commands against the daemon's state, not against the containers directly.

## Practical implications

- If `docker` commands fail with something like `Cannot connect to the Docker daemon at unix:///var/run/docker.sock` — the daemon isn't running (start Docker Desktop, or `sudo systemctl start docker` on Linux).
- The daemon runs as root by default, which is why `docker` commands often need `sudo` unless your user is in the `docker` group — worth noting since the project's Dockerfile itself correctly drops to a non-root `app` user *inside* the container, but that's a separate concern from daemon privileges on the host.
- Since the daemon persists containers/images independently of your shell, that's why `docker-run.sh`'s `docker rm -f` cleanup step at the top is needed — a previous run's container sticks around until you explicitly remove it.
