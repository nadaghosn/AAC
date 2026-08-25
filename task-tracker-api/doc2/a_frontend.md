# Frontend Verification

**How to open the frontend:**
```bash
cd frontend
python -m http.server 5500
```
Then open `http://localhost:5500` in a browser (with the API running separately via `uvicorn app.main:app --reload --port 8000`, since the frontend calls `http://localhost:8000`).

**Confirmation:** Inspected `frontend/index.html` directly and confirmed the three-column Kanban board (`To Do`, `In Progress`, `Done`, each rendered via `data-status` columns) and the create/edit task flow (`New Task` button and `#task-modal` with an `Edit Task` title triggered via `openTaskModal('edit', task)`) are both still present and intact in the markup/JS — no code was changed.
