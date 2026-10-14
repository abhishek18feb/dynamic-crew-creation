from crewai.tools import BaseTool

from flow_practice.models.employee_update import EmployeeUpdateInput
from flow_practice.crews.database.employee_repository import (
    update_employee,
)


class UpdateEmployeeTool(BaseTool):
    name: str = "update_employee"

    description: str = """
    Update an existing employee record in MongoDB.

    Use this tool only when the user explicitly requests an update
    or modification to an existing employee.

    Required:
    - employee_id

    Optional fields:
    - name
    - role
    - email
    - skills
    - resume_path
    - experience_years
    - workload_hours

    Update only the fields explicitly provided by the user.
    Never invent missing values.
    Never create a new employee with this tool.
    """

    args_schema: type[EmployeeUpdateInput] = EmployeeUpdateInput

    def _run(
        self,
        employee_id: str,
        name: str | None = None,
        role: str | None = None,
        email: str | None = None,
        skills: list[str] | None = None,
        resume_path: str | None = None,
        experience_years: int | None = None,
        workload_hours: int | None = None,
    ) -> dict:
        update_input = EmployeeUpdateInput(
            employee_id=employee_id,
            name=name,
            role=role,
            email=email,
            skills=skills,
            resume_path=resume_path,
            experience_years=experience_years,
            workload_hours=workload_hours,
        )

        update_data = update_input.model_dump(
            exclude={"employee_id"},
            exclude_none=True,
        )

        try:
            updated_employee = update_employee(
                employee_id=employee_id,
                update_data=update_data,
            )

            if updated_employee is None:
                return {
                    "success": False,
                    "error": (
                        f"Employee {employee_id} was not found"
                    ),
                }

            return {
                "success": True,
                "message": "Employee updated successfully",
                "employee": updated_employee,
            }

        except ValueError as exc:
            return {
                "success": False,
                "error": str(exc),
            }