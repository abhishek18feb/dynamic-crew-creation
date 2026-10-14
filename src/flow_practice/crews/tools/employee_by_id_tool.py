from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from flow_practice.crews.database.employee_repository import (
    get_employee_by_id,
)


class EmployeeByIdInput(BaseModel):
    employee_id: str = Field(
        description="The exact employee ID to look up, "
                    "for example EMP-BXL03C"
    )


class EmployeeByIdTool(BaseTool):
    name: str = "employee_by_id"

    description: str = """
    Retrieve a single employee using their exact employee ID.

    Use this tool when the user asks for details about a
    particular employee or provides an employee ID.

    Do not use this tool for searching by skills or workload.
    """

    args_schema: type[BaseModel] = EmployeeByIdInput

    def _run(self, employee_id: str) -> dict | str:
        employee = get_employee_by_id(employee_id)

        if employee is None:
            return f"No employee found with ID {employee_id}"

        return employee