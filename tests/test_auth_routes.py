import pytest
import json
from unittest.mock import MagicMock


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