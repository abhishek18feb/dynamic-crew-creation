from crewai.tools import BaseTool

from flow_practice.models.employee_create import EmployeeCreateInput
from flow_practice.crews.database.employee_repository import (
    create_employee,
)


class CreateEmployeeTool(BaseTool):
    name: str = "create_employee"

    description: str = """
    Create a new employee record in MongoDB.

    Use this tool only when the user explicitly asks to create
    or add an employee and the required employee information
    is available.

    Required fields:
    employee_id, name, role, email, skills,
    experience_years, and workload_hours.

    Do not invent missing employee details.
    """

    args_schema: type[EmployeeCreateInput] = EmployeeCreateInput

    def _run(
        self,
        employee_id: str,
        name: str,
        role: str,
        email: str,
        skills: list[str],
        experience_years: int,
        workload_hours: int,
        # resume_path: str = "",
    ) -> dict:

        employee_data = EmployeeCreateInput(
            employee_id=employee_id,
            name=name,
            role=role,
            email=email,
            skills=skills,
            experience_years=experience_years,
            workload_hours=workload_hours,
            # resume_path=resume_path or "",
        )

        try:
            created_employee = create_employee(
                employee_data=employee_data.model_dump()
            )

            return {
                "success": True,
                "message": "Employee created successfully",
                "employee": created_employee,
            }

        except ValueError as exc:
            return {
                "success": False,
                "error": str(exc),
            }