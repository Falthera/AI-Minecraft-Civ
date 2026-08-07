import pytest

from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from inference.app.main import app
    return TestClient(app)


@pytest.mark.asyncio
def test_inference_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200


@pytest.mark.asyncio
def test_inference_models_endpoint(client: TestClient):
    response = client.get("/models", headers={"X-API-Key": "changeme"})
    assert response.status_code == 200
    data = response.json()
    assert "models" in data


@pytest.mark.asyncio
def test_inference_decision_requires_models_loaded(client: TestClient):
    response = client.post("/v1/decision", json={"tier": "fast", "prompt": "test"}, headers={"X-API-Key": "changeme"})
    assert response.status_code == 503


@pytest.mark.asyncio
def test_load_models(client: TestClient):
    response = client.post("/admin/load-models", headers={"X-API-Key": "changeme"})
    assert response.status_code == 200
    response2 = client.post("/v1/decision", json={"tier": "fast", "prompt": "test", "context": {"agent_uuid": "123"}}, headers={"X-API-Key": "changeme"})
    assert response2.status_code == 200
