import json

import pytest
from fastapi.testclient import TestClient

from flow_practice.main import app
from flow_practice.api import routes


class FakeCrewResult:
    def __init__(self, raw):
        self.raw = raw


class FakeEmployeeFlow:
    def __init__(self, raw):
        self.raw = raw
        self.received_inputs = None

    def kickoff(self, inputs):
        self.received_inputs = inputs
        return FakeCrewResult(self.raw)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_employee_search_returns_employees(client, monkeypatch):
    employees = [
        {
            "employee_id": "EMP001",
            "name": "Amit",
            "role": "Developer",
            "skills": ["Python", "React"],
            "workload_hours": 20,
        }
    ]
    fake_flow = FakeEmployeeFlow(json.dumps(employees))

    monkeypatch.setattr(
        routes,
        "EmployeeFlow",
        lambda: fake_flow,
    )

    response = client.post(
        "/employees/search",
        json={"query": "Find Python developers"},
    )

    assert response.status_code == 200
    assert response.json()["query"] == "Find Python developers"
    assert response.json()["employees"] == employees
    assert fake_flow.received_inputs == {
        "query": "Find Python developers"
    }


def test_employee_search_returns_409_for_operation_error(
    client, monkeypatch
):
    fake_flow = FakeEmployeeFlow(
        json.dumps({"error": "Employee creation is not permitted"})
    )

    monkeypatch.setattr(
        routes,
        "EmployeeFlow",
        lambda: fake_flow,
    )

    response = client.post(
        "/employees/search",
        json={"query": "Create an employee"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Employee creation is not permitted"
    )


def test_employee_search_returns_502_for_invalid_output(
    client, monkeypatch
):
    fake_flow = FakeEmployeeFlow("This is not valid JSON or a list")

    monkeypatch.setattr(
        routes,
        "EmployeeFlow",
        lambda: fake_flow,
    )

    response = client.post(
        "/employees/search",
        json={"query": "Find Python developers"},
    )

    assert response.status_code == 502
    assert (
        response.json()["detail"]["message"]
        == "The employee agent returned an unexpected response."
    )


def test_dynamic_employee_search_parses_markdown_table(
    client, monkeypatch
):
    markdown = """\
| Employee ID | Name | Role | Skills | Workload Hours |
| --- | --- | --- | --- | --- |
| EMP001 | Amit | Developer | Python, React | 20 |
"""

    fake_flow = FakeEmployeeFlow(markdown)

    monkeypatch.setattr(
        routes,
        "EmployeeFlowDynamic",
        lambda: fake_flow,
    )

    response = client.post(
        "/employees/search-dynamic",
        json={"query": "Find Python developers"},
    )

    assert response.status_code == 200
    body = response.json()

    assert body["query"] == "Find Python developers"
    assert len(body["employees"]) == 1
    assert body["employees"][0]["employee_id"] == "EMP001"
    assert body["employees"][0]["name"] == "Amit"
    assert body["employees"][0]["skills"] == ["Python", "React"]
    assert body["employees"][0]["workload_hours"] == 20


def test_dynamic_employee_search_returns_502_for_invalid_output(
    client, monkeypatch
):
    fake_flow = FakeEmployeeFlow("Unable to find employees")

    monkeypatch.setattr(
        routes,
        "EmployeeFlowDynamic",
        lambda: fake_flow,
    )

    response = client.post(
        "/employees/search-dynamic",
        json={"query": "Find Python developers"},
    )

    assert response.status_code == 502
    assert (
        response.json()["detail"]["message"]
        == "The employee agent returned an unexpected response."
    )
