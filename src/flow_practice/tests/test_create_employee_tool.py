
import pytest
from pydantic import ValidationError

from flow_practice.crews.tools import create_employee_tool as module
from flow_practice.crews.tools.create_employee_tool import (
    CreateEmployeeTool,
)


@pytest.fixture
def valid_employee_data():
    return {
        "employee_id": "EMP-TEST-001",
        "name": "Test Employee",
        "role": "Python Developer",
        "email": "test.employee@example.com",
        "skills": ["Python", "FastAPI"],
        "experience_years": 3,
        "workload_hours": 20,
    }


def test_create_employee_success(
    monkeypatch,
    valid_employee_data,
):
    expected_employee = {
        **valid_employee_data,
    }

    def fake_create_employee(employee_data):
        assert employee_data == valid_employee_data
        return expected_employee

    monkeypatch.setattr(
        module,
        "create_employee",
        fake_create_employee,
    )

    tool = CreateEmployeeTool()
    result = tool._run(**valid_employee_data)

    assert result["success"] is True
    assert result["message"] == "Employee created successfully"
    assert result["employee"] == expected_employee


def test_create_employee_returns_failure_on_value_error(
    monkeypatch,
    valid_employee_data,
):
    def fake_create_employee(employee_data):
        raise ValueError("Employee ID already exists")

    monkeypatch.setattr(
        module,
        "create_employee",
        fake_create_employee,
    )

    tool = CreateEmployeeTool()
    result = tool._run(**valid_employee_data)

    assert result["success"] is False
    assert result["error"] == "Employee ID already exists"


def test_create_employee_rejects_invalid_input(
    monkeypatch,
    valid_employee_data,
):
    called = False

    def fake_create_employee(employee_data):
        nonlocal called
        called = True
        return employee_data

    monkeypatch.setattr(
        module,
        "create_employee",
        fake_create_employee,
    )

    invalid_data = {
        **valid_employee_data,
        "experience_years": -1,
    }

    tool = CreateEmployeeTool()

    # This test expects the input model to reject negative
    # experience_years. If your model permits it, add that
    # constraint to EmployeeCreateInput first.
    with pytest.raises(ValidationError):
        tool._run(**invalid_data)

    assert called is False


def test_create_employee_propagates_unexpected_exception(
    monkeypatch,
    valid_employee_data,
):
    def fake_create_employee(employee_data):
        raise RuntimeError("Database connection failed")

    monkeypatch.setattr(
        module,
        "create_employee",
        fake_create_employee,
    )

    tool = CreateEmployeeTool()

    with pytest.raises(
        RuntimeError,
        match="Database connection failed",
    ):
        tool._run(**valid_employee_data)

import pytest
from pydantic import ValidationError

from flow_practice.crews.tools import create_employee_tool as module
from flow_practice.crews.tools.create_employee_tool import (
    CreateEmployeeTool,
)


@pytest.fixture
def valid_employee_data():
    return {
        "employee_id": "EMP-TEST-001",
        "name": "Test Employee",
        "role": "Python Developer",
        "email": "test.employee@example.com",
        "skills": ["Python", "FastAPI"],
        "experience_years": 3,
        "workload_hours": 20,
    }


def test_create_employee_success(
    monkeypatch,
    valid_employee_data,
):
    expected_employee = {
        **valid_employee_data,
    }

    def fake_create_employee(employee_data):
        assert employee_data == valid_employee_data
        return expected_employee

    monkeypatch.setattr(
        module,
        "create_employee",
        fake_create_employee,
    )

    tool = CreateEmployeeTool()
    result = tool._run(**valid_employee_data)

    assert result["success"] is True
    assert result["message"] == "Employee created successfully"
    assert result["employee"] == expected_employee


def test_create_employee_returns_failure_on_value_error(
    monkeypatch,
    valid_employee_data,
):
    def fake_create_employee(employee_data):
        raise ValueError("Employee ID already exists")

    monkeypatch.setattr(
        module,
        "create_employee",
        fake_create_employee,
    )

    tool = CreateEmployeeTool()
    result = tool._run(**valid_employee_data)

    assert result["success"] is False
    assert result["error"] == "Employee ID already exists"


def test_create_employee_rejects_invalid_input(
    monkeypatch,
    valid_employee_data,
):
    called = False

    def fake_create_employee(employee_data):
        nonlocal called
        called = True
        return employee_data

    monkeypatch.setattr(
        module,
        "create_employee",
        fake_create_employee,
    )

    invalid_data = {
        **valid_employee_data,
        "experience_years": -1,
    }

    tool = CreateEmployeeTool()

    # This test expects the input model to reject negative
    # experience_years. If your model permits it, add that
    # constraint to EmployeeCreateInput first.
    with pytest.raises(ValidationError):
        tool._run(**invalid_data)

    assert called is False


def test_create_employee_propagates_unexpected_exception(
    monkeypatch,
    valid_employee_data,
):
    def fake_create_employee(employee_data):
        raise RuntimeError("Database connection failed")

    monkeypatch.setattr(
        module,
        "create_employee",
        fake_create_employee,
    )

    tool = CreateEmployeeTool()

    with pytest.raises(
        RuntimeError,
        match="Database connection failed",
    ):
        tool._run(**valid_employee_data)
