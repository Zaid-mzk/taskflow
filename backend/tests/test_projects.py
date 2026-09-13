def test_create_and_list_projects(client, auth_headers):
    resp = client.post(
        "/api/projects", json={"name": "Website Redesign", "description": "Q4 project"}, headers=auth_headers
    )
    assert resp.status_code == 201
    assert resp.get_json()["name"] == "Website Redesign"

    resp = client.get("/api/projects", headers=auth_headers)
    assert resp.status_code == 200
    projects = resp.get_json()
    assert len(projects) == 1
    assert projects[0]["task_counts"]["total"] == 0


def test_create_project_requires_name(client, auth_headers):
    resp = client.post("/api/projects", json={"description": "no name"}, headers=auth_headers)
    assert resp.status_code == 400


def test_get_single_project(client, auth_headers):
    create = client.post("/api/projects", json={"name": "Proj"}, headers=auth_headers)
    project_id = create.get_json()["id"]
    resp = client.get(f"/api/projects/{project_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["id"] == project_id


def test_delete_project(client, auth_headers):
    create = client.post("/api/projects", json={"name": "Proj"}, headers=auth_headers)
    project_id = create.get_json()["id"]
    resp = client.delete(f"/api/projects/{project_id}", headers=auth_headers)
    assert resp.status_code == 200

    resp = client.get(f"/api/projects/{project_id}", headers=auth_headers)
    assert resp.status_code == 404


def test_project_not_visible_to_other_user(client, auth_headers):
    create = client.post("/api/projects", json={"name": "Private"}, headers=auth_headers)
    project_id = create.get_json()["id"]

    client.post(
        "/api/auth/signup",
        json={"username": "dave", "email": "dave@example.com", "password": "password1"},
    )
    login = client.post("/api/auth/login", json={"email": "dave@example.com", "password": "password1"})
    other_headers = {"Authorization": f"Bearer {login.get_json()['token']}"}

    resp = client.get(f"/api/projects/{project_id}", headers=other_headers)
    assert resp.status_code == 404
