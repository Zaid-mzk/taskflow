import pytest


@pytest.fixture
def project_id(client, auth_headers):
    resp = client.post("/api/projects", json={"name": "Proj"}, headers=auth_headers)
    return resp.get_json()["id"]


def test_create_and_list_tasks(client, auth_headers, project_id):
    resp = client.post(
        f"/api/projects/{project_id}/tasks",
        json={"title": "Write tests", "description": "cover the API", "due_date": "2026-12-01"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.get_json()["status"] == "todo"

    resp = client.get(f"/api/projects/{project_id}/tasks", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1


def test_create_task_requires_title(client, auth_headers, project_id):
    resp = client.post(f"/api/projects/{project_id}/tasks", json={}, headers=auth_headers)
    assert resp.status_code == 400


def test_update_task_status(client, auth_headers, project_id):
    create = client.post(
        f"/api/projects/{project_id}/tasks", json={"title": "Task A"}, headers=auth_headers
    )
    task_id = create.get_json()["id"]

    resp = client.patch(f"/api/tasks/{task_id}", json={"status": "in_progress"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "in_progress"


def test_update_task_invalid_status(client, auth_headers, project_id):
    create = client.post(
        f"/api/projects/{project_id}/tasks", json={"title": "Task A"}, headers=auth_headers
    )
    task_id = create.get_json()["id"]
    resp = client.patch(f"/api/tasks/{task_id}", json={"status": "bogus"}, headers=auth_headers)
    assert resp.status_code == 400


def test_delete_task(client, auth_headers, project_id):
    create = client.post(
        f"/api/projects/{project_id}/tasks", json={"title": "Task A"}, headers=auth_headers
    )
    task_id = create.get_json()["id"]
    resp = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
    assert resp.status_code == 200

    resp = client.get(f"/api/projects/{project_id}/tasks", headers=auth_headers)
    assert resp.get_json() == []


def test_filter_tasks_by_status(client, auth_headers, project_id):
    client.post(f"/api/projects/{project_id}/tasks", json={"title": "A", "status": "todo"}, headers=auth_headers)
    t2 = client.post(
        f"/api/projects/{project_id}/tasks", json={"title": "B"}, headers=auth_headers
    ).get_json()
    client.patch(f"/api/tasks/{t2['id']}", json={"status": "done"}, headers=auth_headers)

    resp = client.get(f"/api/projects/{project_id}/tasks?status=done", headers=auth_headers)
    assert len(resp.get_json()) == 1
    assert resp.get_json()[0]["title"] == "B"
