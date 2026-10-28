
import pytest
from pydantic import ValidationError

from flow_practice.crews.tools import delete_employee_tool as module
from flow_practice.crews.tools.delete_employee_tool import (
    DeleteEmployeeTool,
)


@pytest.fixture
def employee_id():
    return "EMP-TEST-001"


def test_delete_employee_rejected_without_confirmation(
    monkeypatch,
    employee_id,
):
    called = False

    def fake_delete_employee(**kwargs):
        nonlocal called
        called = True

    monkeypatch.setattr(
        module,
        "delete_employee",
        fake_delete_employee,
    )

    result = DeleteEmployeeTool()._run(
        employee_id=employee_id,
        confirm_delete=False,
    )

    assert result["success"] is False
    assert "Explicit confirmation is required" in result["error"]
    assert called is False


def test_delete_employee_success(
    monkeypatch,
    employee_id,
):
    expected_employee = {
        "employee_id": employee_id,
        "name": "Test Employee",
    }

    def fake_delete_employee(**kwargs):
        assert kwargs == {"employee_id": employee_id}
        return expected_employee

    monkeypatch.setattr(
        module,
        "delete_employee",
        fake_delete_employee,
    )

    result = DeleteEmployeeTool()._run(
        employee_id=employee_id,
        confirm_delete=True,
    )

    assert result["success"] is True
    assert result["message"] == "Employee deleted successfully."
    assert result["employee"] == expected_employee


def test_delete_employee_not_found(
    monkeypatch,
    employee_id,
):
    monkeypatch.setattr(
        module,
        "delete_employee",
        lambda **kwargs: None,
    )

    result = DeleteEmployeeTool()._run(
        employee_id=employee_id,
        confirm_delete=True,
    )

    assert result["success"] is False
    assert result["error"] == (
        f"Employee {employee_id} was not found."
    )


def test_delete_employee_handles_unexpected_exception(
    monkeypatch,
    employee_id,
):
    def fake_delete_employee(**kwargs):
        raise RuntimeError("Database connection failed")

    monkeypatch.setattr(
        module,
        "delete_employee",
        fake_delete_employee,
    )

    result = DeleteEmployeeTool()._run(
        employee_id=employee_id,
        confirm_delete=True,
    )

    assert result["success"] is False
    assert result["error"] == (
        "An unexpected error occurred during deletion."
    )


def test_delete_employee_rejects_empty_employee_id(
    employee_id,
):
    with pytest.raises(ValidationError):
        DeleteEmployeeTool()._run(
            employee_id="",
            confirm_delete=True,
        )


def test_delete_employee_confirmation_defaults_to_false(
    monkeypatch,
    employee_id,
):
    called = False

    def fake_delete_employee(**kwargs):
        nonlocal called
        called = True

    monkeypatch.setattr(
        module,
        "delete_employee",
        fake_delete_employee,
    )

    result = DeleteEmployeeTool()._run(
        employee_id=employee_id,
    )

    assert result["success"] is False
    assert called is False
