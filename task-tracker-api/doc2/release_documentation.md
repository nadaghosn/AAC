# Release Evidence — Documentation Claim-vs-Reality Log

| Claim checked | Evidence used | Result | Change made if any |
|---|---|---|---|
| `health()` docstring example ends in `+00:00` | Live `TestClient.get("/health")` call | ❌ Mismatch — actual output ends in `Z`, not `+00:00` (Pydantic v2 default serialization) | Fixed: `app/main.py:126` example updated to end in `Z` |
| Docstrings claim `HTTPException: 404` for several routes, implying it's a documented API response | Dumped live `/openapi.json` — checked `responses` keys for all affected routes | ❌ Gap — 404 is never declared in the OpenAPI schema (no route sets `responses={404: ...}`), so it doesn't appear in Swagger UI even though it happens at runtime | None — flagged as an open decision item (declare it in OpenAPI, or document the gap) |
| README: `title` is required and non-blank on both create **and** update | Live `TestClient` PATCH with `{"title": "   "}` | ✅ Claim accurate, but no automated test covered the PATCH+blank-title case (only omit and explicit-null were tested) | Fixed: added `test_patch_blank_title_returns_422_and_keeps_title` to `tests/test_tasks.py` |
| README: status transitions `ToDo→InProgress`, `InProgress→Done`, `Done→InProgress`, same-status no-ops, else `422` | `app/business_rules.py:5-12` (`VALID_TRANSITIONS`) | ✅ Matches exactly | None |
| POST returns `201`, DELETE returns `204` | Route decorators (`status_code=status.HTTP_201_CREATED` / `HTTP_204_NO_CONTENT`) + live `/openapi.json` response codes | ✅ Matches exactly | None |
| Schema names (`TaskCreate`, `TaskUpdate`, `TaskResponse`, `CommentCreate`, `CommentUpdate`, `CommentResponse`, `HealthResponse`) | Live `/openapi.json` `components.schemas` keys | ✅ All present verbatim, no naming drift | None |
| CI workflow summary (triggers, steps, "doesn't build Docker") | Direct read of `../.github/workflows/ci.yml` | ✅ Matches exactly; also confirmed the file is tracked and present on `final-project` (not just referenced in commit messages) | None |
| `TaskUpdate.normalize_tags`'s note: explicit `tags: null` causes a downstream `422` | Live `TestClient` PATCH `{"tags": null}` | ✅ Confirmed — returns `422` via `pydantic.ValidationError` (a `ValueError` subclass) from `TaskResponse.model_validate` re-validation | None — already documented accurately in `app/storage.py` and `app/models.py` |
