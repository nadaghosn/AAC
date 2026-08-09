# Entry point for the Task Tracker API.
# Creates the FastAPI app instance and defines the /health endpoint.

import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.models import TaskCreate, TaskResponse
from app.schemas import HealthResponse
from app.models import TaskStatus, TaskPriority
from typing import Optional

from app.models import TaskUpdate  # add to existing models import
from app.business_rules import validate_status_transition

# Load variables from .env into the process environment (e.g. PORT, APP_ENV).
load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")

app = FastAPI(
    title="Task Tracker API",
    description="Module 1 learning project: a simple in-memory Task Tracker REST API.",
    version="0.1.0",
)

# CORS middleware - allow only the listed origins and open methods/headers per requirements
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
) -> list[TaskResponse]:
    return storage.get_all_tasks(status=status, priority=priority)


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    return storage.add_task(payload)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return task



@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task with id {task_id} not found",
            )
        validate_status_transition(existing.status, payload.status)

    updated = storage.update_task(task_id, payload)
    if updated is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
    deleted = storage.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
