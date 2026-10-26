import pytest
from fastapi.testclient import TestClient

from flow_practice.main import app
from flow_practice.api.task_config_routes import get_task_repository


class FakeTaskRepository:
    def __init__(self):
        self.tasks = {
            "task-001": {
                "task_id": "task-001",
                "name": "Employee Research",
                "description": "Find employees matching the query",
                "expected_output": "A list of matching employees",
                "agent_id": "agent-001",
                "is_active": True,
                "async_execution": False,
                "human_input": False,
            }
        }

    def create(self, config):
        task = config.model_dump()
        task_id = task["task_id"]

        if task_id in self.tasks:
            raise ValueError(f"Task '{task_id}' already exists")

        self.tasks[task_id] = task
        return task

    def get_by_id(self, task_id):
        return self.tasks.get(task_id)

    def list_active(self):
        return [
            task
            for task in self.tasks.values()
            if task.get("is_active", False)
        ]


@pytest.fixture
def fake_task_repository():
    return FakeTaskRepository()


@pytest.fixture
def client(fake_task_repository):
    app.dependency_overrides[get_task_repository] = (
        lambda: fake_task_repository
    )

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


def test_get_existing_task_returns_200(client):
    response = client.get("/task-configs/task-001")

    assert response.status_code == 200
    assert response.json()["task_id"] == "task-001"


def test_get_missing_task_returns_404(client):
    response = client.get("/task-configs/unknown-task")

    assert response.status_code == 404
    assert "was not found" in response.json()["detail"]


def test_list_active_tasks_returns_200(client):
    response = client.get("/task-configs")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["task_id"] == "task-001"


def test_create_task_returns_201(client):
    payload = {
        "task_id": "task-002",
        "name": "Python Employee Search",
        "description": "Search for employees with Python experience",
        "expected_output": "Matching employees with their skills",
        "agent_id": "agent-001",
    }

    response = client.post("/task-configs", json=payload)

    assert response.status_code == 201
    assert response.json()["task_id"] == "task-002"
    assert response.json()["async_execution"] is False


def test_create_duplicate_task_returns_409(client):
    payload = {
        "task_id": "task-001",
        "name": "Duplicate Task",
        "description": "A duplicate task for testing",
        "expected_output": "A list of employees",
        "agent_id": "agent-001",
    }

    response = client.post("/task-configs", json=payload)

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_create_task_with_invalid_payload_returns_422(client):
    payload = {
        "task_id": "",
        "name": "Invalid Task",
        "description": "Search employees",
        "expected_output": "Employee list",
        "agent_id": "agent-001",
    }

    response = client.post("/task-configs", json=payload)

    assert response.status_code == 422
