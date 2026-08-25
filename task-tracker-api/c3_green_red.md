# Module 4 CI Proof — Green → Red → Green (Merged)

Merged from `c3_step1.md` through `c3_step6.md`.

## Step 1 — Confirm branch and clean tree

**Command run:**
```bash
cd /home/esu-linux/AAC
git branch --show-current
git status --short
git log -1 --oneline
```

**Result:**
- Branch: `final-project`
- Working tree: not fully clean — `task-tracker-api/c3.md` was untracked (the checklist file created for this proof)
- HEAD: `f19af7f` ("Add Module 4 CI safety review for ci.yml")

## Step 2 — Pick the smallest assertion to break

**Command run:** None — selection only, no file edited yet.

**Result:** Chose `tests/test_tasks.py:10`, inside `test_create_task_valid_returns_201_with_full_body`:
```python
assert response.status_code == 201
```
Selected because it's the first assertion in the first test, doesn't cascade into other tests, and only touches a test expectation (the route itself still correctly returns `201`).

## Step 3 — The exact one-line change

**Command run:** None — description only, no file edited yet.

**Result:** Planned change to `tests/test_tasks.py:10`:
```python
# current (passes):
assert response.status_code == 201

# change to (fails):
assert response.status_code == 200
```
Chosen because the route actually returns `201 Created`, so asserting `== 200` creates a guaranteed, deterministic mismatch.

## Step 4 — Confirm the failure locally

**Command run:**
```bash
pytest tests/test_tasks.py::test_create_task_valid_returns_201_with_full_body -v
```

**Result:**
```
>       assert response.status_code == 200
E       assert 201 == 200
E        +  where 201 = <Response [201 Created]>.status_code

tests/test_tasks.py:10: AssertionError
FAILED tests/test_tasks.py::test_create_task_valid_returns_201_with_full_body
```
pytest exit code: 1 (checked directly, not through a pipe).

**Command run (full-suite sanity check):**
```bash
pytest -v
```

**Result:** `1 failed, 43 passed in 0.63s` — confirms the break is isolated to the intended test.

## Step 5 — Commit/push the intentional red run

**Command run:**
```bash
git add task-tracker-api/tests/test_tasks.py
git commit -m "Intentional test break for Module 4 CI red-run proof"
git push origin final-project
```

**Result:**
- Commit: `87b77e5` "Intentional test break for Module 4 CI red-run proof"
- Pushed: `f19af7f..87b77e5  final-project -> final-project`
- CI run: [`32773511926`](https://github.com/nadaghosn/AAC/actions/runs/32773511926) — **FAILURE**

CI log evidence:
```
tests/test_tasks.py:10: in test_create_task_valid_returns_201_with_full_body
    assert response.status_code == 200
E   assert 201 == 200
E    +  where 201 = <Response [201 Created]>.status_code
FAILED tests/test_tasks.py::test_create_task_valid_returns_201_with_full_body - assert 201 == 200
========================= 1 failed, 43 passed in 0.29s =========================
##[error]Process completed with exit code 1.
```

## Step 6 — Restore and confirm final green run

**Command run:**
```bash
git revert HEAD --no-edit
pytest -v
git push origin final-project
```

**Result:**
- Revert commit: `3c1c978` "Revert 'Intentional test break for Module 4 CI red-run proof'"
- Local: `pytest -v` → **44 passed** (line 10 restored to `assert response.status_code == 201`)
- Pushed: `87b77e5..3c1c978  final-project -> final-project`
- CI run: [`32773921444`](https://github.com/nadaghosn/AAC/actions/runs/32773921444) — **SUCCESS**

**Full Green → Red → Green summary:**

| Commit | State | CI Run | Result |
|---|---|---|---|
| `f19af7f` (baseline) | green | `32771773869` | SUCCESS |
| `87b77e5` (intentional break) | red | `32773511926` | FAILURE — `assert 201 == 200` |
| `3c1c978` (revert) | green | `32773921444` | SUCCESS |
