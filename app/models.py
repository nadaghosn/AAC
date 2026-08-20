from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _normalize_tags(value) -> List[str]:
    if value is None:
        raw_items = []
    elif isinstance(value, str):
        raw_items = value.split(",")
    else:
        raw_items = list(value)

    normalized: List[str] = []
    seen = set()
    for item in raw_items:
        tag = str(item).strip().lower()
        if not tag:
            continue  # blank / whitespace-only values are ignored
        if tag not in seen:
            seen.add(tag)
            normalized.append(tag)
    return normalized


def _normalize_comment_text(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise ValueError("comment text must not be blank")
    return stripped
    


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class CommentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return _normalize_comment_text(value)


class CommentUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return _normalize_comment_text(value)


class CommentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str
    created_at: datetime


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    comment: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("title must not be blank")
        if len(stripped) > 200:
            raise ValueError("title must be at most 200 characters")
        return stripped

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, value):
        return _normalize_tags(value)

    @field_validator("comment", mode="before")
    @classmethod
    def validate_comment(cls, value):
        # Option A: omit / null / blank / whitespace => no comment
        if value is None:
            return None
        if isinstance(value, str) and not value.strip():
            return None
        return _normalize_comment_text(str(value))


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    tags: Optional[List[str]] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value):
        # Option A: omit title => no change; explicit null => rejected.
        # Omitted fields use the default without running this validator.
        if value is None:
            raise ValueError("title is required")
        stripped = str(value).strip()
        if not stripped:
            raise ValueError("title must not be blank")
        if len(stripped) > 200:
            raise ValueError("title must be at most 200 characters")
        return stripped

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, value):
        if value is None:
            return None
        return _normalize_tags(value)


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    tags: List[str]
    comment: Optional[CommentResponse] = None
    created_at: datetime
    updated_at: datetime
