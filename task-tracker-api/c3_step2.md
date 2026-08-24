# Module 4 CI Proof — Step 2: Pick the smallest assertion to break

## Target

`tests/test_tasks.py:10`, inside `test_create_task_valid_returns_201_with_full_body`:

```python
assert response.status_code == 201
```

## Why this one

- It's the first assertion in the first test — easy to locate and revert.
- Doesn't cascade into other tests; nothing downstream depends on this specific check.
- Only touches a test expectation — the route itself still correctly returns `201`, so no production code is involved.

## Status

No file has been edited yet. This step is selection only.
