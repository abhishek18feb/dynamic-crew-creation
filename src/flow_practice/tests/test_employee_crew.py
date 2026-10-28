
from unittest.mock import MagicMock, patch

from crewai import Process

from flow_practice.employee_crew import create_employee_crew


@patch("flow_practice.employee_crew.Crew")
@patch("flow_practice.employee_crew.Task")
def test_create_employee_crew_configures_task_and_crew(
    mock_task_class,
    mock_crew_class,
):
    mock_task = MagicMock()
    mock_task_class.return_value = mock_task

    mock_crew = MagicMock()
    mock_crew_class.return_value = mock_crew

    query = "Find Python developers with workload under 20 hours"

    result = create_employee_crew(query)

    # Verify the task contains the user's query and expected instructions.
    task_kwargs = mock_task_class.call_args.kwargs
    assert query in task_kwargs["description"]
    assert "create_employee" in task_kwargs["description"]
    assert "update_employee" in task_kwargs["description"]
    assert "delete_employee" in task_kwargs["description"]
    assert "confirmation" in task_kwargs["description"].lower()
    assert task_kwargs["agent"] is not None
    assert task_kwargs["expected_output"]

    # Verify the crew configuration.
    crew_kwargs = mock_crew_class.call_args.kwargs
    assert len(crew_kwargs["agents"]) == 1
    assert crew_kwargs["tasks"] == [mock_task]
    assert crew_kwargs["process"] == Process.sequential
    assert crew_kwargs["verbose"] is True

    assert result is mock_crew


@patch("flow_practice.employee_crew.Crew")
@patch("flow_practice.employee_crew.Task")
def test_create_employee_crew_preserves_query_in_task_description(
    mock_task_class,
    mock_crew_class,
):
    query = "Update EMP-101 workload_hours to 15"

    create_employee_crew(query)

    description = mock_task_class.call_args.kwargs["description"]

    assert query in description
    assert "Do not overwrite fields" in description
    assert "Never delete an employee" in description
