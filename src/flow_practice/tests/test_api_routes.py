import pytest
from fastapi.testclient import TestClient

from flow_practice.main import app
from flow_practice.api.llm_config_routes import get_llm_repository


@pytest.fixture
def client():
    app.dependency_overrides.clear()

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Employee Intelligence API is running"
    }


class FakeLLMRepository:
    """Fake repository for isolated API tests."""

    def list_active_chat_models(self):
        return [
            {
                "llm_config_id": "test-qwen",
                "name": "Test Qwen",
                "provider": "ollama",
                "model_name": "qwen3:2b",
                "model_type": "chat",
                "is_active": True,
            }
        ]

    def get_by_id(self, llm_config_id):
        return None


def test_llm_dropdown_returns_active_chat_models(client):
    app.dependency_overrides[get_llm_repository] = (
        lambda: FakeLLMRepository()
    )

    response = client.get("/llm-configs/dropdown")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["llm_config_id"] == "test-qwen"
    assert data[0]["model_type"] == "chat"


def test_get_missing_llm_config_returns_404(client):
    app.dependency_overrides[get_llm_repository] = (
        lambda: FakeLLMRepository()
    )

    response = client.get("/llm-configs/does-not-exist")

    assert response.status_code == 404
    assert "was not found" in response.json()["detail"]