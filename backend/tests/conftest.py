import pytest
from app import create_app
from app.config import TestConfig
from app.extensions import db


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def signup_and_login(client, username="alice", email="alice@example.com", password="secret123"):
    client.post(
        "/api/auth/signup",
        json={"username": username, "email": email, "password": password},
    )
    resp = client.post("/api/auth/login", json={"email": email, "password": password})
    token = resp.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers(client):
    return signup_and_login(client)
