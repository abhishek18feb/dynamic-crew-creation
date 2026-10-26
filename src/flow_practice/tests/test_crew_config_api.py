import pytest
from fastapi.testclient import TestClient

from flow_practice.main import app
from flow_practice.api.crew_config_routes import get_crew_repository


class FakeCrewRepository:
    def __init__(self):
        self.crews = {
            "crew-001": {
                "crew_id": "crew-001",
                "name": "Employee Research Crew",
                "description": "Find matching employees",
                "task_ids": ["task-001"],
                "process": "sequential",
                "is_active": True,
                "verbose": True,
            }
        }

    def create(self, config):
        crew = config.model_dump()
        crew_id = crew["crew_id"]

        if crew_id in self.crews:
            raise ValueError(f"Crew '{crew_id}' already exists")

        self.crews[crew_id] = crew
        return crew

    def get_by_id(self, crew_id):
        return self.crews.get(crew_id)

    def list_active(self):
        return [
            crew
            for crew in self.crews.values()
            if crew.get("is_active", False)
        ]


@pytest.fixture
def fake_crew_repository():
    return FakeCrewRepository()


@pytest.fixture
def client(fake_crew_repository):
    app.dependency_overrides[get_crew_repository] = (
        lambda: fake_crew_repository
    )

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


def test_get_existing_crew_returns_200(client):
    response = client.get("/crew-configs/crew-001")

    assert response.status_code == 200
    assert response.json()["crew_id"] == "crew-001"


def test_get_missing_crew_returns_404(client):
    response = client.get("/crew-configs/unknown-crew")

    assert response.status_code == 404
    assert "was not found" in response.json()["detail"]


def test_list_active_crews_returns_200(client):
    response = client.get("/crew-configs")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["crew_id"] == "crew-001"


def test_create_crew_returns_201(client):
    payload = {
        "crew_id": "crew-002",
        "name": "Python Research Crew",
        "description": "Research Python developers",
        "task_ids": ["task-001", "task-002"],
    }

    response = client.post("/crew-configs", json=payload)

    assert response.status_code == 201
    assert response.json()["crew_id"] == "crew-002"
    assert response.json()["process"] == "sequential"


def test_create_duplicate_crew_returns_409(client):
    payload = {
        "crew_id": "crew-001",
        "name": "Duplicate Crew",
        "task_ids": ["task-001"],
    }

    response = client.post("/crew-configs", json=payload)

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_create_crew_with_duplicate_task_ids_returns_422(client):
    payload = {
        "crew_id": "crew-003",
        "name": "Invalid Crew",
        "task_ids": ["task-001", "task-001"],
    }

    response = client.post("/crew-configs", json=payload)

    assert response.status_code == 422


def test_create_crew_without_task_ids_returns_422(client):
    payload = {
        "crew_id": "crew-004",
        "name": "Crew Without Tasks",
        "task_ids": [],
    }

    response = client.post("/crew-configs", json=payload)

    assert response.status_code == 422


def test_create_crew_with_unsupported_process_returns_422(client):
    payload = {
        "crew_id": "crew-005",
        "name": "Unsupported Process Crew",
        "task_ids": ["task-001"],
        "process": "hierarchical",
    }

    response = client.post("/crew-configs", json=payload)

    assert response.status_code == 422
