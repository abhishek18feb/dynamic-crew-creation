
from flow_practice.crews.tools.employee_search_tool import (
    EmployeeSearchTool,
)
from flow_practice.crews.tools.employee_by_id_tool import (
    EmployeeByIdTool,
)
from flow_practice.crews.tools.create_employee_tool import (
    CreateEmployeeTool,
)
from flow_practice.crews.tools.update_employee_tool import (
    UpdateEmployeeTool,
)
from flow_practice.crews.tools.delete_employee_tool import (
    DeleteEmployeeTool,
)


def get_tool_registry() -> dict:
    return {
        "employee_search": EmployeeSearchTool(),
        "employee_by_id": EmployeeByIdTool(),
        "create_employee": CreateEmployeeTool(),
        "update_employee": UpdateEmployeeTool(),
        "delete_employee": DeleteEmployeeTool(),
    }


def resolve_tools(tool_ids: list[str]) -> list:
    registry = get_tool_registry()

    unknown_tools = set(tool_ids) - set(registry)

    if unknown_tools:
        raise ValueError(
            f"Unsupported tool IDs: {sorted(unknown_tools)}"
        )

    return [registry[tool_id] for tool_id in tool_ids]
