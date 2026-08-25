# Documentation Audit — Corrections Applied (Follow-up to doc2_claims.md)

Summary of the corrections made after reviewing `doc2_claims.md`'s findings 1 and 3.

## Corrections

| Claim | Fix applied | Files touched |
|---|---|---|
| **#1 — timestamp format** | `health()` docstring example changed from `"...+00:00"` to `"...Z"`, matching the actual Pydantic v2 serialization observed live | `app/main.py` |
| **#3 — PATCH+blank-title coverage gap** | Added `test_patch_blank_title_returns_422_and_keeps_title`, mirroring the POST blank-title test's pattern; confirms `422` and that the title is left unchanged | `tests/test_tasks.py` |
| **Test count references** | Updated "44 tests" → "45 tests" now that the new test exists | `README.md`, `doc2_claims.md` |
| **#2 — 404 not in OpenAPI schema** | Left open — marked as a decision item, not a fix, in `doc2_claims.md` | `doc2_claims.md` (status note only) |

## Verification

- Fresh `TestClient.get("/health")` call confirmed the `Z`-suffixed format matches the corrected docstring example.
- Full pytest suite run after both changes: 45 passed (44 original + the new PATCH+blank-title test).

## Status

Findings 1 and 3 from `doc2_claims.md` are fixed. Finding 2 (404 not declared in the OpenAPI schema) remains open — a decision is needed on whether to add explicit `responses={404: {...}}` to the affected route decorators or just document the gap. Nothing has been committed yet.
