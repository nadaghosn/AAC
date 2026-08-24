# Module 4 CI Proof — Step 5: Commit/push the intentional red run

## Commands run

```bash
git add task-tracker-api/tests/test_tasks.py
git commit -m "Intentional test break for Module 4 CI red-run proof"
git push origin final-project
```

(Only the test file was staged — the c3*.md planning docs were left uncommitted to keep the red-run commit isolated and clean.)

## Result

- Commit: `87b77e5` "Intentional test break for Module 4 CI red-run proof"
- Pushed: `f19af7f..87b77e5  final-project -> final-project`
- CI run: [`32773511926`](https://github.com/nadaghosn/AAC/actions/runs/32773511926) — **FAILURE**

## CI log evidence

```
tests/test_tasks.py:10: in test_create_task_valid_returns_201_with_full_body
    assert response.status_code == 200
E   assert 201 == 200
E    +  where 201 = <Response [201 Created]>.status_code
FAILED tests/test_tasks.py::test_create_task_valid_returns_201_with_full_body - assert 201 == 200
========================= 1 failed, 43 passed in 0.29s =========================
##[error]Process completed with exit code 1.
```

## Conclusion

CI correctly failed on a genuine test failure — a real red run, distinct from the earlier billing-lock failures seen on the old account.
