from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models import (
    CommentCreate,
    CommentResponse,
    CommentUpdate,
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)

_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    now = datetime.now(timezone.utc)
    task = TaskResponse(
        id=str(uuid4()),
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        tags=payload.tags,
        comment=CommentResponse(text=payload.comment, created_at=now),
        created_at=now,
        updated_at=now,
    )
    _tasks[task.id] = task
    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    tag: Optional[str] = None,
) -> list[TaskResponse]:
    results = list(_tasks.values())
    if status is not None:
        results = [task for task in results if task.status == status]
    if priority is not None:
        results = [task for task in results if task.priority == priority]
    if tag is not None:
        normalized_tag = tag.strip().lower()
        results = [task for task in results if normalized_tag in task.tags]
    return results


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    existing = _tasks.get(task_id)
    if existing is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return existing

    updated = existing.model_copy(
        update={**updates, "updated_at": datetime.now(timezone.utc)}
    )
    _tasks[task_id] = updated
    return updated


def delete_task(task_id: str) -> bool:
    if task_id not in _tasks:
        return False
    del _tasks[task_id]
    return True


def get_comment(task_id: str) -> tuple[bool, Optional[CommentResponse]]:
    task = _tasks.get(task_id)
    if task is None:
        return False, None
    return True, task.comment


def add_comment(task_id: str, payload: CommentCreate) -> Optional[CommentResponse]:
    task = _tasks.get(task_id)
    if task is None:
        return None
    if task.comment is not None:
        raise ValueError("task already has a comment")

    comment = CommentResponse(
        text=payload.text,
        created_at=datetime.now(timezone.utc),
    )
    _tasks[task_id] = task.model_copy(
        update={"comment": comment, "updated_at": datetime.now(timezone.utc)}
    )
    return comment


def update_comment(task_id: str, payload: CommentUpdate) -> Optional[CommentResponse]:
    task = _tasks.get(task_id)
    if task is None or task.comment is None:
        return None

    comment = CommentResponse(
        text=payload.text,
        created_at=task.comment.created_at,
    )
    _tasks[task_id] = task.model_copy(
        update={"comment": comment, "updated_at": datetime.now(timezone.utc)}
    )
    return comment


def replace_comment(task_id: str, payload: CommentUpdate) -> Optional[CommentResponse]:
    task = _tasks.get(task_id)
    if task is None:
        return None
    if task.comment is None:
        return None

    comment = CommentResponse(
        text=payload.text,
        created_at=task.comment.created_at,
    )
    _tasks[task_id] = task.model_copy(
        update={"comment": comment, "updated_at": datetime.now(timezone.utc)}
    )
    return comment


def delete_comment(task_id: str) -> bool:
    task = _tasks.get(task_id)
    if task is None:
        return False
    raise ValueError("comment is required and cannot be removed")


def _reset() -> None:
    _tasks.clear()
