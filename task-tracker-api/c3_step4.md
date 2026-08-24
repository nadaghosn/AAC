# Module 4 CI Proof — Step 4: Confirm the failure locally

## Edit applied

`tests/test_tasks.py:10`:
```python
assert response.status_code == 200   # was 201
```

## Command

```bash
pytest tests/test_tasks.py::test_create_task_valid_returns_201_with_full_body -v
```

## Result

```
>       assert response.status_code == 200
E       assert 201 == 200
E        +  where 201 = <Response [201 Created]>.status_code

tests/test_tasks.py:10: AssertionError
FAILED tests/test_tasks.py::test_create_task_valid_returns_201_with_full_body
```

**pytest exit code: 1** (checked directly, not through a pipe, so nothing hid the real exit status)

## Full-suite sanity check

```bash
pytest -v
```
Result: `1 failed, 43 passed in 0.63s` — confirms the break is isolated to the intended test; nothing else regressed.

## Status

Working tree now has one intentional uncommitted change: `tests/test_tasks.py`. Not yet committed or pushed.
