def test_create_task_valid_returns_201_with_full_body(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Buy milk",
            "tags": ["errands"],
            "comment": "Pick up 2%",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Buy milk"
    assert body["description"] == ""
    assert body["status"] == "ToDo"
    assert body["priority"] == "Medium"
    assert body["assignee"] is None
    assert body["tags"] == ["errands"]
    assert body["comment"]["text"] == "Pick up 2%"
    assert "created_at" in body["comment"]
    assert "id" in body
    assert "created_at" in body
    assert "updated_at" in body


def test_create_task_missing_title_returns_422(client):
    response = client.post(
        "/tasks",
        json={"tags": ["backend"], "comment": "note"},
    )
    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client):
    response = client.post(
        "/tasks",
        json={"title": "   ", "tags": ["backend"], "comment": "note"},
    )
    assert response.status_code == 422


def test_create_task_without_comment_returns_201_with_null_comment(client):
    response = client.post(
        "/tasks",
        json={"title": "Task", "tags": ["backend"]},
    )
    assert response.status_code == 201
    assert response.json()["comment"] is None


def test_create_task_blank_comment_treated_as_no_comment(client):
    response = client.post(
        "/tasks",
        json={"title": "Task", "tags": ["backend"], "comment": "   "},
    )
    assert response.status_code == 201
    assert response.json()["comment"] is None


def test_create_task_without_tags_returns_201_with_empty_tags(client):
    response = client.post("/tasks", json={"title": "No tags"})
    assert response.status_code == 201
    body = response.json()
    assert body["tags"] == []
    assert body["comment"] is None


def test_create_task_invalid_priority_returns_422(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Task",
            "priority": "Urgent",
            "tags": ["backend"],
            "comment": "note",
        },
    )
    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Task",
            "tags": ["backend"],
            "comment": "note",
            "unknown": "value",
        },
    )
    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client):
    client.post("/tasks", json={"title": "todo task", "tags": ["general"]})
    response = client.get("/tasks", params={"status": "Done"})
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    client.post(
        "/tasks",
        json={
            "title": "low",
            "priority": "Low",
            "tags": ["general"],
            "comment": "note",
        },
    )
    client.post(
        "/tasks",
        json={
            "title": "high",
            "priority": "High",
            "tags": ["general"],
            "comment": "note",
        },
    )
    response = client.get("/tasks", params={"priority": "High"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["title"] == "high"
    assert body[0]["priority"] == "High"


def test_get_task_by_id_returns_task(client, created_task):
    response = client.get(f"/tasks/{created_task['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created_task["id"]
    assert response.json()["title"] == "fixture task"
    assert response.json()["tags"] == ["general"]
    assert response.json()["comment"]["text"] == "fixture comment"


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    task_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {task_id} not found"


def test_patch_partial_update_keeps_other_fields(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"title": "updated title"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "updated title"
    assert body["description"] == created_task["description"]
    assert body["status"] == created_task["status"]
    assert body["priority"] == created_task["priority"]
    assert body["assignee"] == created_task["assignee"]
    assert body["tags"] == created_task["tags"]
    assert body["comment"] == created_task["comment"]
    assert body["id"] == created_task["id"]


def test_patch_explicit_null_title_returns_422_and_keeps_title(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"title": None},
    )
    assert response.status_code == 422
    get_response = client.get(f"/tasks/{created_task['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "fixture task"


def test_patch_omit_title_keeps_existing_title(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"priority": "Low"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "fixture task"
    assert response.json()["priority"] == "Low"


def test_patch_not_found_returns_404(client):
    task_id = "00000000-0000-0000-0000-000000000000"
    response = client.patch(f"/tasks/{task_id}", json={"title": "nope"})
    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {task_id} not found"


def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "InProgress"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_status_keeps_comment_unchanged(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "InProgress"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "InProgress"
    assert body["comment"]["text"] == created_task["comment"]["text"]
    assert body["comment"]["created_at"] == created_task["comment"]["created_at"]


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "Done"},
    )
    assert response.status_code == 422


def test_patch_same_status_returns_200(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "ToDo"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ToDo"


def test_delete_existing_returns_204_no_body(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    task_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 404


# --- TAG-002: edit tags on a task ---

def test_patch_tags_add_remove_replace_persists(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"tags": ["backend", "api"]},
    )
    assert response.status_code == 200
    assert response.json()["tags"] == ["backend", "api"]

    get_response = client.get(f"/tasks/{created_task['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["tags"] == ["backend", "api"]


def test_patch_tags_accepts_comma_separated_string(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"tags": "Frontend, Docs"},
    )
    assert response.status_code == 200
    assert response.json()["tags"] == ["frontend", "docs"]


def test_patch_tags_not_found_returns_404(client):
    task_id = "00000000-0000-0000-0000-000000000000"
    response = client.patch(f"/tasks/{task_id}", json={"tags": ["backend"]})
    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {task_id} not found"


# --- TAG-003: filter tasks by tag ---

def test_list_tasks_filter_by_tag_returns_only_matches(client):
    client.post(
        "/tasks",
        json={
            "title": "API work",
            "description": "Build endpoints",
            "priority": "High",
            "assignee": "Ada",
            "tags": ["backend", "api"],
            "comment": "api note",
        },
    )
    client.post(
        "/tasks",
        json={"title": "UI polish", "tags": ["frontend"], "comment": "ui note"},
    )
    response = client.get("/tasks", params={"tag": "backend"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    task = body[0]
    assert task["title"] == "API work"
    assert "id" in task
    assert task["status"] == "ToDo"
    assert task["priority"] == "High"
    assert task["description"] == "Build endpoints"
    assert task["assignee"] == "Ada"
    assert task["tags"] == ["backend", "api"]
    assert task["comment"]["text"] == "api note"


def test_list_tasks_filter_by_tag_no_match_returns_empty_list(client):
    client.post(
        "/tasks",
        json={"title": "UI polish", "tags": ["frontend"], "comment": "ui note"},
    )
    response = client.get("/tasks", params={"tag": "backend"})
    assert response.status_code == 200
    assert response.json() == []


# --- TAG-004: replace/remove tags with at least one remaining ---

def test_patch_remove_tag_when_others_remain_keeps_other_fields(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Tagged task",
            "description": "keep me",
            "priority": "Low",
            "assignee": "Grace",
            "tags": ["backend", "api"],
            "comment": "keep comment",
        },
    )
    task = create_response.json()

    response = client.patch(
        f"/tasks/{task['id']}",
        json={"tags": ["api"]},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["tags"] == ["api"]
    assert body["title"] == task["title"]
    assert body["description"] == task["description"]
    assert body["status"] == task["status"]
    assert body["priority"] == task["priority"]
    assert body["assignee"] == task["assignee"]
    assert body["comment"] == task["comment"]
    assert body["id"] == task["id"]


def test_patch_replace_tag_keeps_other_fields(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Replace tags",
            "description": "unchanged",
            "priority": "Medium",
            "assignee": "Linus",
            "tags": ["legacy"],
            "comment": "keep comment",
        },
    )
    task = create_response.json()

    response = client.patch(
        f"/tasks/{task['id']}",
        json={"tags": ["modern"]},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["tags"] == ["modern"]
    assert body["title"] == task["title"]
    assert body["description"] == task["description"]
    assert body["status"] == task["status"]
    assert body["priority"] == task["priority"]
    assert body["assignee"] == task["assignee"]
    assert body["comment"] == task["comment"]


def test_patch_remove_all_tags_returns_200(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"tags": []},
    )
    assert response.status_code == 200
    assert response.json()["tags"] == []


# --- TAG-005: prevent duplicate / blank tags ---

def test_create_task_duplicate_tags_are_deduplicated(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Dedup",
            "tags": [" Urgent ", "urgent", "Backend"],
            "comment": "note",
        },
    )
    assert response.status_code == 201
    assert response.json()["tags"] == ["urgent", "backend"]


def test_patch_adding_existing_tag_does_not_duplicate(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"tags": ["General", " general ", "api"]},
    )
    assert response.status_code == 200
    assert response.json()["tags"] == ["general", "api"]


def test_create_task_blank_tags_are_ignored(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Blank tag",
            "tags": ["valid", "  ", ""],
            "comment": "note",
        },
    )
    assert response.status_code == 201
    assert response.json()["tags"] == ["valid"]


def test_patch_blank_tags_are_ignored(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"tags": ["ok", ""]},
    )
    assert response.status_code == 200
    assert response.json()["tags"] == ["ok"]


def test_create_task_only_blank_tags_becomes_empty_list(client):
    response = client.post(
        "/tasks",
        json={"title": "Only blanks", "tags": ["", "   "]},
    )
    assert response.status_code == 201
    assert response.json()["tags"] == []


# --- Comments ---

def test_get_comment_returns_comment(client, created_task):
    response = client.get(f"/tasks/{created_task['id']}/comments")
    assert response.status_code == 200
    assert response.json()["text"] == "fixture comment"
    assert "created_at" in response.json()


def test_add_second_comment_returns_422(client, created_task):
    response = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "another"},
    )
    assert response.status_code == 422


def test_patch_comment_updates_text(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "updated note"},
    )
    assert response.status_code == 200
    assert response.json()["text"] == "updated note"

    task = client.get(f"/tasks/{created_task['id']}").json()
    assert task["comment"]["text"] == "updated note"


def test_patch_comment_blank_text_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "   "},
    )
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail


def test_patch_comment_not_found_returns_404(client):
    task_id = "00000000-0000-0000-0000-000000000000"
    response = client.patch(
        f"/tasks/{task_id}/comments",
        json={"text": "updated note"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == f"Comment for task id {task_id} not found"


def test_add_comment_on_task_without_comment_returns_201(client):
    create_response = client.post("/tasks", json={"title": "No comment yet"})
    task_id = create_response.json()["id"]
    response = client.post(
        f"/tasks/{task_id}/comments",
        json={"text": "added later"},
    )
    assert response.status_code == 201
    assert response.json()["text"] == "added later"


def test_delete_comment_returns_204_and_clears_comment(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}/comments")
    assert response.status_code == 204
    task = client.get(f"/tasks/{created_task['id']}").json()
    assert task["comment"] is None


def test_delete_comment_when_none_returns_404(client):
    create_response = client.post("/tasks", json={"title": "No comment"})
    task_id = create_response.json()["id"]
    response = client.delete(f"/tasks/{task_id}/comments")
    assert response.status_code == 404
