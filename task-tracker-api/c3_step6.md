# Module 4 CI Proof — Step 6: Restore and confirm final green run

## Commands run

```bash
git revert HEAD --no-edit
pytest -v
git push origin final-project
```

## Result

- Revert commit: `3c1c978` "Revert 'Intentional test break for Module 4 CI red-run proof'"
- Local: `pytest -v` → **44 passed** (line 10 of `tests/test_tasks.py` restored to `assert response.status_code == 201`)
- Pushed: `87b77e5..3c1c978  final-project -> final-project`
- CI run: [`32773921444`](https://github.com/nadaghosn/AAC/actions/runs/32773921444) — **SUCCESS**

## Full Green → Red → Green proof (final-project branch)

| Commit | State | CI Run | Result |
|---|---|---|---|
| `f19af7f` (baseline) | green | `32771773869` | SUCCESS |
| `87b77e5` (intentional break) | red | `32773511926` | FAILURE — `assert 201 == 200` |
| `3c1c978` (revert) | green | `32773921444` | SUCCESS |

## Conclusion

CI on `nadaghosn/AAC` correctly fails when a test assertion is wrong and passes again once the code is restored. This closes out the Module 4 CI proof.
