# Project Summary

- The project is a Python Task Tracker REST API with a FastAPI application entry point. Evidence: [app/main.py](../app/main.py#L32) creates the app as "Task Tracker API," and [requirements.txt](../requirements.txt#L1) pins FastAPI, Uvicorn, and Pydantic.

- It provides task collection and item operations: list (with status, priority, and tag filters), create, read by ID, update, and delete. Evidence: [app/main.py](../app/main.py#L80) defines `GET /tasks`; [app/main.py](../app/main.py#L89), [app/main.py](../app/main.py#L94), [app/main.py](../app/main.py#L106), and [app/main.py](../app/main.py#L132) define the remaining CRUD routes.

- Tasks have structured fields and input validation, including status, priority, tags, optional comments, and timestamps. Evidence: [app/models.py](../app/models.py#L77) defines the task-create schema; [app/models.py](../app/models.py#L88) rejects blank or over-200-character titles; [app/models.py](../app/models.py#L146) defines the returned task fields.

- Runtime data is held in an in-memory dictionary, with UUID task IDs and UTC creation/update timestamps; persistence across restarts is not evidenced. Evidence: [app/storage.py](../app/storage.py#L16) declares `_tasks` as a dictionary, while [app/storage.py](../app/storage.py#L19) creates UUIDs and timestamps before storing tasks.

- It includes a browser-based Kanban-style frontend and automated pytest CI. Evidence: [frontend/index.html](../frontend/index.html#L398) defines To Do, In Progress, and Done columns, while its JavaScript targets `/tasks` at [frontend/index.html](../frontend/index.html#L479). [ci.yml](../../.github/workflows/ci.yml#L3) runs on pushes and pull requests and executes `pytest` at [ci.yml](../../.github/workflows/ci.yml#L34).

## Documentation Note

[README.md](../README.md#L3) says task CRUD is not implemented, which conflicts with the current source files above; the README appears outdated.
