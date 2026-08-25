# Test Baseline — Full pytest Suite Run

## Command run

```bash
pytest -v
```
(run from `task-tracker-api/`)

## Result

```
45 passed in 0.78s
```

Full suite, zero failures.

## Failing tests

None. No pre-existing-vs-introduced-by-final-work distinction is needed, since nothing failed.

## Full output

```
============================= test session starts ==============================
platform linux -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0 -- /home/esu-linux/AAC/task-tracker-api/venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/esu-linux/AAC/task-tracker-api
plugins: anyio-4.14.2
collecting ... collected 45 items

tests/test_tasks.py::test_create_task_valid_returns_201_with_full_body PASSED [  2%]
tests/test_tasks.py::test_create_task_missing_title_returns_422 PASSED   [  4%]
tests/test_tasks.py::test_create_task_blank_title_returns_422 PASSED     [  6%]
tests/test_tasks.py::test_create_task_without_comment_returns_201_with_null_comment PASSED [  8%]
tests/test_tasks.py::test_create_task_blank_comment_treated_as_no_comment PASSED [ 11%]
tests/test_tasks.py::test_create_task_without_tags_returns_201_with_empty_tags PASSED [ 13%]
tests/test_tasks.py::test_create_task_invalid_priority_returns_422 PASSED [ 15%]
tests/test_tasks.py::test_create_task_unknown_field_returns_422 PASSED   [ 17%]
tests/test_tasks.py::test_list_tasks_empty_returns_200_and_empty_list PASSED [ 20%]
tests/test_tasks.py::test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list PASSED [ 22%]
tests/test_tasks.py::test_list_tasks_filter_by_priority_returns_only_matches PASSED [ 24%]
tests/test_tasks.py::test_get_task_by_id_returns_task PASSED             [ 26%]
tests/test_tasks.py::test_get_task_by_id_not_found_returns_404_with_detail PASSED [ 28%]
tests/test_tasks.py::test_patch_partial_update_keeps_other_fields PASSED [ 31%]
tests/test_tasks.py::test_patch_explicit_null_title_returns_422_and_keeps_title PASSED [ 33%]
tests/test_tasks.py::test_patch_blank_title_returns_422_and_keeps_title PASSED [ 35%]
tests/test_tasks.py::test_patch_omit_title_keeps_existing_title PASSED   [ 37%]
tests/test_tasks.py::test_patch_not_found_returns_404 PASSED             [ 40%]
tests/test_tasks.py::test_patch_valid_transition_todo_to_inprogress_returns_200 PASSED [ 42%]
tests/test_tasks.py::test_patch_status_keeps_comment_unchanged PASSED    [ 44%]
tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422 PASSED [ 46%]
tests/test_tasks.py::test_patch_same_status_returns_200 PASSED           [ 48%]
tests/test_tasks.py::test_delete_existing_returns_204_no_body PASSED     [ 51%]
tests/test_tasks.py::test_delete_missing_returns_404 PASSED              [ 53%]
tests/test_tasks.py::test_patch_tags_add_remove_replace_persists PASSED  [ 55%]
tests/test_tasks.py::test_patch_tags_accepts_comma_separated_string PASSED [ 57%]
tests/test_tasks.py::test_patch_tags_not_found_returns_404 PASSED        [ 60%]
tests/test_tasks.py::test_list_tasks_filter_by_tag_returns_only_matches PASSED [ 62%]
tests/test_tasks.py::test_list_tasks_filter_by_tag_no_match_returns_empty_list PASSED [ 64%]
tests/test_tasks.py::test_patch_remove_tag_when_others_remain_keeps_other_fields PASSED [ 66%]
tests/test_tasks.py::test_patch_replace_tag_keeps_other_fields PASSED    [ 68%]
tests/test_tasks.py::test_patch_remove_all_tags_returns_200 PASSED       [ 71%]
tests/test_tasks.py::test_create_task_duplicate_tags_are_deduplicated PASSED [ 73%]
tests/test_tasks.py::test_patch_adding_existing_tag_does_not_duplicate PASSED [ 75%]
tests/test_tasks.py::test_create_task_blank_tags_are_ignored PASSED      [ 77%]
tests/test_tasks.py::test_patch_blank_tags_are_ignored PASSED            [ 80%]
tests/test_tasks.py::test_create_task_only_blank_tags_becomes_empty_list PASSED [ 82%]
tests/test_tasks.py::test_get_comment_returns_comment PASSED             [ 84%]
tests/test_tasks.py::test_add_second_comment_returns_422 PASSED          [ 86%]
tests/test_tasks.py::test_patch_comment_updates_text PASSED              [ 88%]
tests/test_tasks.py::test_patch_comment_blank_text_returns_422 PASSED    [ 91%]
tests/test_tasks.py::test_patch_comment_not_found_returns_404 PASSED     [ 93%]
tests/test_tasks.py::test_add_comment_on_task_without_comment_returns_201 PASSED [ 95%]
tests/test_tasks.py::test_delete_comment_returns_204_and_clears_comment PASSED [ 97%]
tests/test_tasks.py::test_delete_comment_when_none_returns_404 PASSED    [100%]

============================== 45 passed in 0.78s ==============================
```
