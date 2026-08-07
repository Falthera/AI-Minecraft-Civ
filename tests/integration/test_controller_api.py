import pytest

from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from controller.app.main import app
    return TestClient(app)


@pytest.mark.asyncio
def test_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
def test_create_agent(client: TestClient):
    response = client.post("/agents", json={"username": "TestBot"}, headers={"X-API-Key": "changeme"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "TestBot"
    assert data["life_state"] == "ACTIVE"


@pytest.mark.asyncio
def test_api_auth_required(client: TestClient):
    response = client.post("/agents", json={"username": "NoAuth"})
    assert response.status_code == 401
