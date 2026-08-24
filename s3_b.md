# Proposed diff for `GET /version` (not applied — plan only)

No files have been edited. This is the exact diff I would apply, shown for review before any implementation.

## `app/main.py`

Insert the new route between the existing `json_version()` handler (ends `app/main.py:69`) and the `health()` handler (starts `app/main.py:72`), matching the file's existing two-blank-line spacing between top-level route functions.

```diff
--- a/app/main.py
+++ b/app/main.py
@@ -67,6 +67,12 @@
         "name": app.title,
         "version": app.version,
     }
 
 
+@app.get("/version", tags=["root"])
+def version() -> dict:
+    return {"version": app.version}
+
+
 @app.get("/health", response_model=HealthResponse, tags=["health"])
 def health() -> HealthResponse:
     return HealthResponse(
```

## `tests/test_tasks.py`

Append a new test at the end of the file (currently 514 lines, ends with `test_delete_comment_when_none_returns_404`), following the file's existing two-blank-line separation between tests and its plain `def test_name(client):` pattern (no imports needed — `client` is injected via the `conftest.py` fixture, same as every other test in the file).

```diff
--- a/tests/test_tasks.py
+++ b/tests/test_tasks.py
@@ -511,3 +511,9 @@
     task_id = create_response.json()["id"]
     response = client.delete(f"/tasks/{task_id}/comments")
     assert response.status_code == 404
+
+
+def test_get_version_returns_200_and_version_key(client):
+    response = client.get("/version")
+    assert response.status_code == 200
+    assert "version" in response.json()
```

Note: the test asserts the `version` key exists rather than hard-coding `"0.1.0"`, so it doesn't need updating every time `app.version` is bumped in `app/main.py:35`.

## How you would test it

1. **Automated (primary):**
   ```bash
   pytest -v
   ```
   Confirms the new test passes and — just as importantly — that all 44 existing tests still pass unchanged, i.e. the new route doesn't collide with any existing path or break app startup.

2. **Manual (optional, for a quick eyeball check):**
   ```bash
   uvicorn app.main:app --reload --port 8000
   curl http://localhost:8000/version
   ```
   Expect `{"version":"0.1.0"}` (or whatever `app.version` currently is) and a `200` status. You can also hit `http://localhost:8000/docs` and confirm `/version` shows up under the `root` tag alongside `/` and `/json/version`.

3. **Regression check:** specifically re-run the existing `/json/version` behavior (no dedicated test currently exists for it, so this would be a manual `curl http://localhost:8000/json/version`) to confirm the new route didn't shadow or interfere with it — they're separate paths, but worth eyeballing once since both return version info.

## Still waiting on your approval before applying either diff.
