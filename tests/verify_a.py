import sys
from pathlib import Path

from pydantic import ValidationError

# Project root must be on sys.path so `from app...` works when run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models import (
    TaskCreate,
    TaskUpdate,
    TaskStatus,
    TaskPriority,
    CommentCreate,
    CommentUpdate,
)


def expect_fail(label, fn):
    try:
        fn()
        print(f"FAIL: {label} — value was accepted but should have been rejected")
    except ValidationError:
        print(f"PASS: {label}")


def expect_ok(label, fn):
    try:
        fn()
        print(f"PASS: {label}")
    except Exception as e:
        print(f"FAIL: {label} — {e}")


# 1. Whitespace title rejected
expect_fail(
    "whitespace title rejected",
    lambda: TaskCreate(title=" ", tags=["x"], comment="c"),
)

# 2. Empty title rejected
expect_fail(
    "empty title rejected",
    lambda: TaskCreate(title="", tags=["x"], comment="c"),
)

# 3. Title over 200 chars rejected
expect_fail(
    "title > 200 chars rejected",
    lambda: TaskCreate(title="x" * 201, tags=["x"], comment="c"),
)

# 4. Valid title accepted, defaults applied
def _ok_defaults():
    t = TaskCreate(title="Hello", tags=["general"], comment="hello note")
    assert t.status == TaskStatus.TODO
    assert t.priority == TaskPriority.MEDIUM
    assert t.description == ""
    assert t.assignee is None
    assert t.tags == ["general"]
    assert t.comment == "hello note"


expect_ok(
    "defaults applied (status=ToDo, priority=Medium, description='')",
    _ok_defaults,
)

# 5. extra='forbid' — unknown field rejected on TaskCreate
expect_fail(
    "extra field rejected on TaskCreate",
    lambda: TaskCreate(title="x", tags=["x"], comment="c", made_up="value"),
)

# 6. id NOT settable via TaskCreate
expect_fail(
    "id rejected on TaskCreate",
    lambda: TaskCreate(title="x", tags=["x"], comment="c", id="abc"),
)

# 7. created_at NOT settable via TaskUpdate
expect_fail(
    "created_at rejected on TaskUpdate",
    lambda: TaskUpdate(created_at="2025-01-01T00:00:00Z"),
)

# 8. Invalid enum value rejected
expect_fail(
    "invalid status rejected",
    lambda: TaskCreate(title="x", tags=["x"], comment="c", status="Whatever"),
)

# 9. Blank tag value rejected
expect_fail(
    "blank tag value rejected",
    lambda: TaskCreate(title="x", tags=["valid", "  "], comment="c"),
)

# 10. Tags trimmed and normalized (whitespace stripped, case-folded, duplicates removed)
def _ok_tags_normalized():
    t = TaskCreate(
        title="x",
        tags=[" Urgent ", "urgent", "Backend"],
        comment="c",
    )
    assert t.tags == ["urgent", "backend"]


expect_ok("tags trimmed, lowercased, and de-duplicated", _ok_tags_normalized)

# 11. Blank comment text rejected on CommentCreate
expect_fail("blank comment text rejected", lambda: CommentCreate(text="   "))

# 12. Valid comment text accepted and trimmed
def _ok_comment_text():
    c = CommentCreate(text="  Needs review  ")
    assert c.text == "Needs review"
    u = CommentUpdate(text="  Updated note  ")
    assert u.text == "Updated note"


expect_ok("comment text accepted and trimmed", _ok_comment_text)

# 13. Missing required comment on TaskCreate rejected
expect_fail(
    "missing comment on TaskCreate rejected",
    lambda: TaskCreate(title="x", tags=["x"]),
)

# 14. Blank comment on TaskCreate rejected
expect_fail(
    "blank comment on TaskCreate rejected",
    lambda: TaskCreate(title="x", tags=["x"], comment="   "),
)

# 15. Comment on TaskCreate trimmed
def _ok_task_comment_trimmed():
    t = TaskCreate(title="x", tags=["x"], comment="  required note  ")
    assert t.comment == "required note"


expect_ok("task create comment trimmed", _ok_task_comment_trimmed)

print("--- Part A verifications complete ---")
