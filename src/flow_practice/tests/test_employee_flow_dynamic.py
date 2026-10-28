
from unittest.mock import MagicMock, patch

import pytest

from flow_practice.employee_flow_dynamic import EmployeeFlowDynamic


def test_kickoff_builds_crew_and_passes_trimmed_query():
    with patch(
        "flow_practice.employee_flow_dynamic.CrewBuilder"
    ) as mock_builder_class:
        mock_builder = mock_builder_class.return_value
        mock_crew = MagicMock()
        mock_builder.build_crew.return_value = mock_crew
        mock_crew.kickoff.return_value = "Employee search result"

        flow = EmployeeFlowDynamic()
        result = flow.kickoff({
            "query": "  Find Python developers  "
        })

        mock_builder.build_crew.assert_called_once_with(
            "employee_management_crew"
        )
        mock_crew.kickoff.assert_called_once_with(
            inputs={"query": "Find Python developers"}
        )
        assert result == "Employee search result"


@pytest.mark.parametrize(
    "inputs",
    [
        {},
        {"query": ""},
        {"query": "   "},
        {"query": None},
        {"query": 123},
        {"query": ["Python"]},
    ],
)
def test_kickoff_rejects_invalid_query(inputs):
    flow = EmployeeFlowDynamic()

    with pytest.raises(
        ValueError,
        match="A non-empty employee query is required",
    ):
        flow.kickoff(inputs)


def test_kickoff_propagates_crew_builder_error():
    with patch(
        "flow_practice.employee_flow_dynamic.CrewBuilder"
    ) as mock_builder_class:
        mock_builder_class.return_value.build_crew.side_effect = (
            RuntimeError("Crew configuration failed")
        )

        flow = EmployeeFlowDynamic()

        with pytest.raises(
            RuntimeError,
            match="Crew configuration failed",
        ):
            flow.kickoff({"query": "Find Python developers"})


def test_kickoff_propagates_crew_execution_error():
    with patch(
        "flow_practice.employee_flow_dynamic.CrewBuilder"
    ) as mock_builder_class:
        mock_crew = MagicMock()
        mock_builder_class.return_value.build_crew.return_value = (
            mock_crew
        )
        mock_crew.kickoff.side_effect = RuntimeError(
            "Crew execution failed"
        )

        flow = EmployeeFlowDynamic()

        with pytest.raises(
            RuntimeError,
            match="Crew execution failed",
        ):
            flow.kickoff({"query": "Find Python developers"})
