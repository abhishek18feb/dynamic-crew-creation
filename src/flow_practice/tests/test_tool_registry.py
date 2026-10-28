
import pytest

from flow_practice.crews.tools import tool_registry as module
from flow_practice.crews.tools.tool_registry import (
    get_tool_registry,
    resolve_tools,
)


class FakeTool:
    def __init__(self, name):
        self.name = name


@pytest.fixture
def fake_registry(monkeypatch):
    registry = {
        "employee_search": FakeTool("employee_search"),
        "employee_by_id": FakeTool("employee_by_id"),
        "create_employee": FakeTool("create_employee"),
        "update_employee": FakeTool("update_employee"),
        "delete_employee": FakeTool("delete_employee"),
    }

    monkeypatch.setattr(
        module,
        "get_tool_registry",
        lambda: registry,
    )

    return registry


def test_get_tool_registry_contains_expected_tools():
    registry = get_tool_registry()

    expected_tools = {
        "employee_search",
        "employee_by_id",
        "create_employee",
        "update_employee",
        "delete_employee",
    }

    assert set(registry.keys()) == expected_tools


def test_resolve_tools_returns_requested_tools_in_order(fake_registry):
    tools = resolve_tools(
        ["employee_search", "employee_by_id"]
    )

    assert [tool.name for tool in tools] == [
        "employee_search",
        "employee_by_id",
    ]


def test_resolve_tools_rejects_unknown_tool_id(fake_registry):
    with pytest.raises(
        ValueError,
        match="Unsupported tool IDs",
    ):
        resolve_tools(["unknown_tool"])


def test_resolve_tools_rejects_mixed_valid_and_invalid_ids(
    fake_registry,
):
    with pytest.raises(
        ValueError,
        match="Unsupported tool IDs",
    ):
        resolve_tools(
            ["employee_search", "unknown_tool"]
        )


def test_resolve_tools_returns_empty_list_for_empty_input(
    fake_registry,
):
    assert resolve_tools([]) == []
