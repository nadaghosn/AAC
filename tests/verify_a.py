import sys
from pathlib import Path

from pydantic import ValidationError

# Project root must be on sys.path so `from app...` works when run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models import TaskCreate, TaskUpdate, TaskStatus, TaskPriority
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
expect_fail("whitespace title rejected", lambda: TaskCreate(title=" ", tags=["x"]))

# 2. Empty title rejected
expect_fail("empty title rejected", lambda: TaskCreate(title="", tags=["x"]))

# 3. Title over 200 chars rejected
expect_fail("title > 200 chars rejected", lambda: TaskCreate(title="x" * 201, tags=["x"]))

# 4. Valid title accepted, defaults applied
def _ok_defaults():
  t = TaskCreate(title="Hello", tags=["general"])
  assert t.status == TaskStatus.TODO
  assert t.priority == TaskPriority.MEDIUM
  assert t.description == ""
  assert t.assignee is None
  assert t.tags == ["general"]

expect_ok("defaults applied (status=ToDo, priority=Medium, description='')",
_ok_defaults)

# 5. extra='forbid' — unknown field rejected on TaskCreate
expect_fail("extra field rejected on TaskCreate", lambda: TaskCreate(title="x",
tags=["x"], made_up="value"))

# 6. id NOT settable via TaskCreate
expect_fail("id rejected on TaskCreate", lambda: TaskCreate(title="x", tags=["x"], id="abc"))

# 7. created_at NOT settable via TaskUpdate
expect_fail("created_at rejected on TaskUpdate", lambda: TaskUpdate(created_at="2025-01-01T00:00:00Z"))

# 8. Invalid enum value rejected
expect_fail("invalid status rejected", lambda: TaskCreate(title="x", tags=["x"], status="Whatever"))

# 9. Blank tag value rejected
expect_fail("blank tag value rejected", lambda: TaskCreate(title="x", tags=["valid", "  "]))

# 10. Tags trimmed and normalized (whitespace stripped, case-folded, duplicates removed)
def _ok_tags_normalized():
    t = TaskCreate(title="x", tags=[" Urgent ", "urgent", "Backend"])
    assert t.tags == ["urgent", "backend"]

expect_ok("tags trimmed, lowercased, and de-duplicated", _ok_tags_normalized)

print("--- Part A verifications complete ---")
