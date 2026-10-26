
import pytest
from fastapi.testclient import TestClient

from flow_practice.main import app
from flow_practice.api.crew_execution_routes import get_crew_builder


class FakeCrew:
    def __init__(self, result="Found 2 matching employees"):
        self.result = result
        self.received_inputs = None

    def kickoff(self, inputs):
        self.received_inputs = inputs
        return self.result


class FakeCrewBuilder:
    def __init__(self, crew=None, error=None):
        self.crew = crew or FakeCrew()
        self.error = error
        self.requested_crew_id = None

    def build_crew(self, crew_id):
        self.requested_crew_id = crew_id

        if self.error:
            raise self.error

        return self.crew


@pytest.fixture
def client():
    app.dependency_overrides.clear()

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


def test_run_crew_successfully(client):
    fake_crew = FakeCrew(result="Found 2 matching employees")
    fake_builder = FakeCrewBuilder(crew=fake_crew)

    app.dependency_overrides[get_crew_builder] = (
        lambda: fake_builder
    )

    payload = {
        "inputs": {
            "query": "Find Python developers"
        }
    }

    response = client.post(
        "/crews/employee_management_crew/run",
        json=payload,
    )

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "crew_id": "employee_management_crew",
        "result": "Found 2 matching employees",
    }

    assert fake_builder.requested_crew_id == "employee_management_crew"
    assert fake_crew.received_inputs == {
        "query": "Find Python developers"
    }


def test_run_unknown_crew_returns_400(client):
    fake_builder = FakeCrewBuilder(
        error=ValueError("Crew configuration not found")
    )

    app.dependency_overrides[get_crew_builder] = (
        lambda: fake_builder
    )

    response = client.post(
        "/crews/unknown_crew/run",
        json={"inputs": {}},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Crew configuration not found"


def test_run_crew_unexpected_error_returns_500(client):
    fake_builder = FakeCrewBuilder(
        error=RuntimeError("Simulated execution failure")
    )

    app.dependency_overrides[get_crew_builder] = (
        lambda: fake_builder
    )

    response = client.post(
        "/crews/employee_management_crew/run",
        json={"inputs": {}},
    )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Crew execution failed. Check application logs."
    )
