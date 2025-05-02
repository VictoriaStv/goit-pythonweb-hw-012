# tests/conftest.py
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(autouse=True, scope="function")   
def mock_redis(monkeypatch):
    mock_redis_instance = MagicMock()
    monkeypatch.setattr("src.routes.auth.redis_client", mock_redis_instance)
