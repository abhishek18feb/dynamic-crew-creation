from crewai.tools import BaseTool
from pydantic import BaseModel, Field

# from flow_practice.crews.database.mongodb import employees_collection
from flow_practice.crews.database.employee_repository import (
    search_employees,
)

class EmployeeSearchInput(BaseModel):

    skills: list[str] = Field(
        description="List of skills to search for"
    )

    max_workload: int = Field(
        description="Maximum workload hours"
    )
    
class EmployeeSearchTool(BaseTool):

    name: str = "employee_search"

    args_schema: type[BaseModel] = EmployeeSearchInput

    description: str = """
    Search employees from MongoDB.

    Use this tool when you need to find employees
    based on one or more skills and maximum workload.

    The search matches ANY of the provided skills.
    """

    def _run(
        self,
        skills: list[str],
        max_workload: int,
    ):

        return search_employees(
            skills=skills,
            max_workload=max_workload,
        )