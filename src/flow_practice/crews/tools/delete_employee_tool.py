from crewai.tools import BaseTool

from flow_practice.models.employee_delete import EmployeeDeleteInput
from flow_practice.crews.database.employee_repository import (
    delete_employee,
)


class DeleteEmployeeTool(BaseTool):
    name: str = "delete_employee"

    description: str = """
    Delete an existing employee record from MongoDB.

    Required arguments:
    - employee_id: the exact employee ID
    - confirm_delete: must be true only after the user explicitly
      confirms deletion of that employee.

    Never delete by name alone.
    Never infer confirmation from a request to merely find or inspect
    an employee.
    If confirmation is false or missing, do not delete anything.
    """

    args_schema: type[EmployeeDeleteInput] = EmployeeDeleteInput

    def _run(
        self,
        employee_id: str,
        confirm_delete: bool = False,
    ) -> dict:
        if not confirm_delete:
            return {
                "success": False,
                "error": (
                    "Deletion not confirmed. Explicit confirmation "
                    f"is required to delete employee {employee_id}."
                ),
            }

        try:
            deleted_employee = delete_employee(
                employee_id=employee_id
            )

            if deleted_employee is None:
                return {
                    "success": False,
                    "error": f"Employee {employee_id} was not found.",
                }

            return {
                "success": True,
                "message": "Employee deleted successfully.",
                "employee": deleted_employee,
            }

        except Exception:
            # Log the underlying exception in your application.
            return {
                "success": False,
                "error": "An unexpected error occurred during deletion.",
            }