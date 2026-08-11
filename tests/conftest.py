# CHANGED: << pytest tests/ -v >>
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Project root must be on sys.path so `from app...` works under pytest.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app
from app import storage


@pytest.fixture(autouse=True)
def _reset_storage():
    storage._reset()
    yield
    storage._reset()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def created_task(client):
    response = client.post(
        "/tasks",
        json={"title": "fixture task", "tags": ["general"]},
    )
    assert response.status_code == 201
    return response.json()
