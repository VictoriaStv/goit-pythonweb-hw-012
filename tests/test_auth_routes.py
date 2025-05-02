import pytest
import json
from unittest.mock import MagicMock
from src.services.auth import create_email_verification_token


def test_signup(client):
    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass123"
    }
    response = client.post("/auth/signup", json=payload)
    assert response.status_code in (201, 400)


def test_login(client, monkeypatch):
    monkeypatch.setattr("src.routes.auth.redis_client", MagicMock())

    login_data = {
        "username": "testuser@example.com",
        "password": "testpass123"
    }
    response = client.post("/auth/login", data=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.fixture()
def access_token(client, monkeypatch):
    monkeypatch.setattr("src.routes.auth.redis_client", MagicMock())
    monkeypatch.setattr("src.services.auth.redis_client", MagicMock())

    login_data = {
        "username": "testuser@example.com",
        "password": "testpass123"
    }
    response = client.post("/auth/login", data=login_data)
    return response.json()["access_token"]


def test_me(client, access_token, monkeypatch):
    mock_redis = MagicMock()
    mock_redis.get.return_value = json.dumps({
        "id": 1,
        "username": "testuser",
        "email": "testuser@example.com",
        "confirmed": True,
        "role": "user"
    })
    monkeypatch.setattr("src.services.auth.redis_client", mock_redis)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/auth/me", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["username"] == "testuser"


def test_me_unauthorized(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_verify_email_valid_token(client, monkeypatch):
    monkeypatch.setattr("src.routes.auth.redis_client", MagicMock())
    monkeypatch.setattr("src.services.auth.redis_client", MagicMock())

    email = "testuser@example.com"
    token = create_email_verification_token(email)

    response = client.get(f"/auth/verify-email?token={token}")
    assert response.status_code in (200, 400)


def test_verify_email_invalid_token(client):
    token = "invalid.token.value"
    response = client.get(f"/auth/verify-email?token={token}")
    assert response.status_code == 400


def test_admin_access_denied(client, access_token, monkeypatch):
    mock_redis = MagicMock()
    mock_redis.get.return_value = json.dumps({
        "id": 1,
        "username": "testuser",
        "email": "testuser@example.com",
        "confirmed": True,
        "role": "user"
    })
    monkeypatch.setattr("src.services.auth.redis_client", mock_redis)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/auth/admin-only", headers=headers)

    assert response.status_code == 403


def test_admin_access_granted(client, access_token, monkeypatch):
    mock_redis = MagicMock()
    mock_redis.get.return_value = json.dumps({
        "id": 1,
        "username": "adminuser",
        "email": "admin@example.com",
        "confirmed": True,
        "role": "admin"
    })
    monkeypatch.setattr("src.services.auth.redis_client", mock_redis)

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/auth/admin-only", headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome, admin!"
