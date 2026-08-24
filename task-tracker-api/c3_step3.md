# Module 4 CI Proof — Step 3: The exact one-line change

## Target

`tests/test_tasks.py:10`

```python
# current (passes):
assert response.status_code == 201

# change to (fails):
assert response.status_code == 200
```

## Why this fails deterministically

The `POST /tasks` route actually returns `201 Created` on success (confirmed by the earlier full-suite run). Asserting `== 200` instead creates a guaranteed mismatch — `AssertionError: assert 201 == 200` — not a flaky or environment-dependent failure.

## Status

No file has been edited yet. This step is description only.
