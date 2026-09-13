def test_signup_success(client):
    resp = client.post(
        "/api/auth/signup",
        json={"username": "bob", "email": "bob@example.com", "password": "password1"},
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert "token" in data
    assert data["user"]["email"] == "bob@example.com"


def test_signup_duplicate_email(client):
    payload = {"username": "bob", "email": "bob@example.com", "password": "password1"}
    client.post("/api/auth/signup", json=payload)
    resp = client.post("/api/auth/signup", json={**payload, "username": "bob2"})
    assert resp.status_code == 409


def test_signup_missing_fields(client):
    resp = client.post("/api/auth/signup", json={"email": "bob@example.com"})
    assert resp.status_code == 400


def test_login_success(client):
    client.post(
        "/api/auth/signup",
        json={"username": "carol", "email": "carol@example.com", "password": "password1"},
    )
    resp = client.post(
        "/api/auth/login", json={"email": "carol@example.com", "password": "password1"}
    )
    assert resp.status_code == 200
    assert "token" in resp.get_json()


def test_login_wrong_password(client):
    client.post(
        "/api/auth/signup",
        json={"username": "carol", "email": "carol@example.com", "password": "password1"},
    )
    resp = client.post(
        "/api/auth/login", json={"email": "carol@example.com", "password": "wrongpass"}
    )
    assert resp.status_code == 401


def test_protected_route_requires_token(client):
    resp = client.get("/api/projects")
    assert resp.status_code == 401
