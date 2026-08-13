from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator


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
            raise ValueError("tags must not contain blank values")
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
    tags: List[str]
    comment: str

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
        normalized = _normalize_tags(value)
        if not normalized:
            raise ValueError("tags must contain at least one tag")
        return normalized

    @field_validator("comment")
    @classmethod
    def validate_comment(cls, value: str) -> str:
        return _normalize_comment_text(value)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    tags: Optional[List[str]] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        stripped = value.strip()
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
        normalized = _normalize_tags(value)
        if not normalized:
            raise ValueError("tags must contain at least one tag")
        return normalized


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    tags: List[str]
    comment: CommentResponse
    created_at: datetime
    updated_at: datetime
