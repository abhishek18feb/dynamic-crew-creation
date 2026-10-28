
import pytest
from pydantic import ValidationError

from flow_practice.crews.tools import update_employee_tool as module
from flow_practice.crews.tools.update_employee_tool import (
    UpdateEmployeeTool,
)


@pytest.fixture
def valid_update_data():
    return {
        "employee_id": "EMP-TEST-001",
        "name": "Updated Employee",
        "role": "Senior Python Developer",
        "email": "updated.employee@example.com",
        "skills": ["Python", "FastAPI"],
        "experience_years": 5,
        "workload_hours": 25,
    }


def test_update_employee_success(
    monkeypatch,
    valid_update_data,
):
    expected_employee = {
        "employee_id": "EMP-TEST-001",
        "name": "Updated Employee",
    }

    def fake_update_employee(employee_id, update_data):
        assert employee_id == "EMP-TEST-001"
        assert update_data == {
            "name": "Updated Employee",
            "role": "Senior Python Developer",
            "email": "updated.employee@example.com",
            "skills": ["Python", "FastAPI"],
            "experience_years": 5,
            "workload_hours": 25,
        }
        return expected_employee

    monkeypatch.setattr(
        module,
        "update_employee",
        fake_update_employee,
    )

    result = UpdateEmployeeTool()._run(**valid_update_data)

    assert result["success"] is True
    assert result["employee"] == expected_employee


def test_update_employee_not_found(
    monkeypatch,
    valid_update_data,
):
    monkeypatch.setattr(
        module,
        "update_employee",
        lambda **kwargs: None,
    )

    result = UpdateEmployeeTool()._run(**valid_update_data)

    assert result["success"] is False
    assert result["error"] == (
        "Employee EMP-TEST-001 was not found"
    )


def test_update_employee_returns_value_error(
    monkeypatch,
    valid_update_data,
):
    def fake_update_employee(**kwargs):
        raise ValueError("Invalid employee update")

    monkeypatch.setattr(
        module,
        "update_employee",
        fake_update_employee,
    )

    result = UpdateEmployeeTool()._run(**valid_update_data)

    assert result["success"] is False
    assert result["error"] == "Invalid employee update"


def test_update_employee_rejects_invalid_email(
    monkeypatch,
    valid_update_data,
):
    called = False

    def fake_update_employee(**kwargs):
        nonlocal called
        called = True

    monkeypatch.setattr(
        module,
        "update_employee",
        fake_update_employee,
    )

    invalid_data = {
        **valid_update_data,
        "email": "not-an-email",
    }

    with pytest.raises(ValidationError):
        UpdateEmployeeTool()._run(**invalid_data)

    assert called is False


def test_update_employee_rejects_negative_experience(
    monkeypatch,
    valid_update_data,
):
    called = False

    def fake_update_employee(**kwargs):
        nonlocal called
        called = True

    monkeypatch.setattr(
        module,
        "update_employee",
        fake_update_employee,
    )

    invalid_data = {
        **valid_update_data,
        "experience_years": -1,
    }

    with pytest.raises(ValidationError):
        UpdateEmployeeTool()._run(**invalid_data)

    assert called is False


def test_update_employee_rejects_empty_employee_id(
    monkeypatch,
    valid_update_data,
):
    called = False

    def fake_update_employee(**kwargs):
        nonlocal called
        called = True

    monkeypatch.setattr(
        module,
        "update_employee",
        fake_update_employee,
    )

    invalid_data = {
        **valid_update_data,
        "employee_id": "",
    }

    with pytest.raises(ValidationError):
        UpdateEmployeeTool()._run(**invalid_data)

    assert called is False


def test_update_employee_propagates_unexpected_exception(
    monkeypatch,
    valid_update_data,
):
    def fake_update_employee(**kwargs):
        raise RuntimeError("Database connection failed")

    monkeypatch.setattr(
        module,
        "update_employee",
        fake_update_employee,
    )

    with pytest.raises(
        RuntimeError,
        match="Database connection failed",
    ):
        UpdateEmployeeTool()._run(**valid_update_data)
