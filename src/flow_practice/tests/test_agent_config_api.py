import pytest
from fastapi.testclient import TestClient

from flow_practice.main import app
from flow_practice.api.agent_config_routes import (
    get_agent_repository,
    get_llm_repository
)


class FakeAgentRepository:
    def __init__(self):
        self.agents = {
            "agent-001": {
                "agent_id": "agent-001",
                "role": "Employee Researcher",
                "goal": "Find employees matching a request",
                "backstory": "An employee research specialist",
                "is_active": True,
            }
        }

    def create(self, config):
        agent = config.model_dump()
        agent_id = agent["agent_id"]

        if agent_id in self.agents:
            raise ValueError(
                f"Agent '{agent_id}' already exists"
            )

        self.agents[agent_id] = agent
        return agent

    def get_by_id(self, agent_id):
        return self.agents.get(agent_id)

    def list_active(self):
        return [
            agent
            for agent in self.agents.values()
            if agent.get("is_active", False)
        ]

    def update_llm_config(self, agent_id, llm_config_id):
        agent = self.agents.get(agent_id)

        if agent is None:
            return False

        agent["llm_config_id"] = llm_config_id
        return True

class FakeLLMRepository:
    def __init__(self):
        self.models = {
            "active_chat": {
                "llm_config_id": "active_chat",
                "name": "Active Chat Model",
                "model_type": "chat",
                "is_active": True,
            },
            "inactive_chat": {
                "llm_config_id": "inactive_chat",
                "name": "Inactive Chat Model",
                "model_type": "chat",
                "is_active": False,
            },
            "active_embedding": {
                "llm_config_id": "active_embedding",
                "name": "Embedding Model",
                "model_type": "embedding",
                "is_active": True,
            },
        }

    def get_by_id(self, llm_config_id):
        return self.models.get(llm_config_id)

@pytest.fixture
def fake_agent_repository():
    return FakeAgentRepository()

@pytest.fixture
def fake_llm_repository():
    return FakeLLMRepository()


@pytest.fixture
def client(fake_agent_repository, fake_llm_repository):
    app.dependency_overrides[get_agent_repository] = (
        lambda: fake_agent_repository
    )
    app.dependency_overrides[get_llm_repository] = (
        lambda: fake_llm_repository
    )

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


def test_get_existing_agent_returns_200(client):
    response = client.get("/agent-configs/agent-001")

    assert response.status_code == 200
    assert response.json()["agent_id"] == "agent-001"


def test_get_missing_agent_returns_404(client):
    response = client.get("/agent-configs/unknown-agent")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_list_active_agents_returns_200(client):
    response = client.get("/agent-configs")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["agent_id"] == "agent-001"



def test_create_agent_returns_201(client):
    payload = {
        "agent_id": "agent-002",
        "name": "Python Researcher",
        "role": "Python Employee Researcher",
        "goal": "Find employees with Python experience",
        "backstory": "An expert at matching employee skills",
        "llm_config_id": "local_ollama",
        "tool_ids": [],
        "allow_delegation": False,
        "verbose": True,
        "is_active": True,
        "max_iter": 10,
    }

    response = client.post("/agent-configs", json=payload)

    assert response.status_code == 201
    assert response.json()["agent_id"] == "agent-002"
    assert response.json()["name"] == "Python Researcher"


def test_create_duplicate_agent_returns_409(client):
    payload = {
        "agent_id": "agent-001",
        "name": "Duplicate Researcher",
        "role": "Employee Researcher",
        "goal": "Find matching employees",
        "backstory": "An employee research specialist",
    }

    response = client.post("/agent-configs", json=payload)

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_create_agent_with_invalid_payload_returns_422(client):
    payload = {
        "agent_id": "",
        "name": "Invalid Researcher",
        "role": "Employee Researcher",
        "goal": "Find matching employees",
        "backstory": "An employee research specialist",
    }

    response = client.post("/agent-configs", json=payload)

    assert response.status_code == 422

def test_update_agent_llm_with_active_chat_model_returns_200(client):
    response = client.patch(
        "/agent-configs/agent-001/llm-config",
        json={"llm_config_id": "active_chat"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "agent_id": "agent-001",
        "llm_config_id": "active_chat",
    }


def test_update_agent_llm_with_missing_model_returns_400(client):
    response = client.patch(
        "/agent-configs/agent-001/llm-config",
        json={"llm_config_id": "unknown_model"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Select an active, configured chat model"
    )


def test_update_agent_llm_with_inactive_model_returns_400(client):
    response = client.patch(
        "/agent-configs/agent-001/llm-config",
        json={"llm_config_id": "inactive_chat"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Select an active, configured chat model"
    )


def test_update_agent_llm_with_embedding_model_returns_400(client):
    response = client.patch(
        "/agent-configs/agent-001/llm-config",
        json={"llm_config_id": "active_embedding"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Select an active, configured chat model"
    )


def test_update_agent_llm_for_missing_agent_returns_404(client):
    response = client.patch(
        "/agent-configs/unknown-agent/llm-config",
        json={"llm_config_id": "active_chat"},
    )

    assert response.status_code == 404
    assert "unknown-agent" in response.json()["detail"]