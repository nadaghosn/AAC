# Dockerfile Decision Summary

## Builder Stage

| Line(s) | Instruction | Decision | Why |
|---|---|---|---|
| 2 | `FROM python:3.11-slim AS builder` | Pinned `3.11-slim` tag, not `latest` | Reproducible builds; slim keeps image lean; matches runtime stage's Python version exactly to avoid build/run mismatches |
| 4 | `WORKDIR /app` | Sets build working directory | Unambiguous destination for `COPY requirements.txt .` |
| 6 | `RUN python -m venv /opt/venv` | Install deps into a venv, not system site-packages | A venv is a self-contained tree that can be copied wholesale into the runtime stage — enables "copy only the virtual environment" |
| 7 | `ENV PATH="/opt/venv/bin:$PATH"` | Prepend venv's `bin/` to PATH | Makes the very next `pip install` target the venv, not the system Python |
| 9 | `COPY requirements.txt .` (before installing) | Copy only the manifest first, not full source | Docker layer caching — code-only changes don't invalidate the dependency-install layer |
| 10 | `RUN pip install --no-cache-dir -r requirements.txt` | `--no-cache-dir` | Keeps pip's download/wheel cache out of the layer; stage is discarded anyway, but keeps build I/O lean |

## Runtime Stage

| Line(s) | Instruction | Decision | Why |
|---|---|---|---|
| 13 | `FROM python:3.11-slim AS runtime` | Fresh base image, same pinned tag | Nothing from the builder's toolchain/cache carries over — only explicit `COPY --from=builder` steps bring anything across |
| 15 | `RUN useradd --uid 1000 --no-create-home --shell /usr/sbin/nologin app` | Fixed UID 1000, no home dir, `nologin` shell | Fixed UID avoids ownership drift across rebuilds/mounts; app is stateless so no home dir needed; `nologin` is defense-in-depth since this user never needs a shell |
| 17 | `WORKDIR /app` | Runtime's own working dir | Independent of builder's `/app` (different filesystem) |
| 19 | `COPY --from=builder /opt/venv /opt/venv` | Copy only the populated venv | Brings in installed dependencies without any build tooling or pip cache |
| 20 | `COPY app ./app` | Copy only the `app/` package | Excludes `tests/`, `docs/`, `frontend/`, `data/`, `.git`, notes files, `venv/`/`.venv/` — by construction, not just via `.dockerignore` |
| 22 | `RUN chown -R app:app /app` | Ownership set after copy, scoped to `/app` only | Satisfies explicit "set ownership of the app directory to app"; venv at `/opt/venv` stays root-owned/world-readable since it's read-only at runtime |
| 24 | `ENV PATH="/opt/venv/bin:$PATH"` (repeated) | Re-declared in this stage | `ENV` doesn't persist across `FROM` boundaries — without this, `uvicorn`/`python` would resolve to the base image's system Python |
| 26 | `USER app` | Switch before any runtime-behavior instructions | Required to precede `CMD`; root never runs the app process |
| 28 | `EXPOSE 8000` | Documentation/metadata only | Doesn't publish the port itself, but declares the contract |
| 32 | `CMD [...] --host 0.0.0.0 --port 8000` | Exec form, no `--reload` | `0.0.0.0` required so traffic from outside the container's namespace can reach it; exec form gives `uvicorn` direct signal handling for graceful shutdown; `--reload` is dev-only and was explicitly excluded |

## HEALTHCHECK

| Decision | Why |
|---|---|
| `--interval=30s --timeout=5s`, no extra flags | Matches spec exactly; no `--start-period`/`--retries` added since they weren't requested |
| Python stdlib (`urllib.request.urlopen`), not `curl` | Spec asked to prefer stdlib unless curl is installed on purpose — avoids adding an `apt-get install` step and extra attack surface |
| Exec form (`CMD [...]`) | No intermediate `/bin/sh -c`; avoids shell-quoting ambiguity with the quotes already inside the Python snippet |
| No explicit `try/except`/`sys.exit` | `urlopen` raises on non-2xx or connection failure; an uncaught exception already makes Python exit non-zero, which is exactly what `HEALTHCHECK` needs |
| Target `http://127.0.0.1:8000/health`, not `0.0.0.0` | Check runs inside the container's own network namespace — `0.0.0.0` is what the server *binds to*; you *connect to* loopback from inside |
