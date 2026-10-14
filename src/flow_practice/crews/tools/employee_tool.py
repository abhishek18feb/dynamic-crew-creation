from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from flow_practice.crews.database.mongodb import employees_collection



class EmployeeSearchTool(BaseTool):

    name: str = "employee_search"

    description: str = """
    Search employees in MongoDB based on skill
    and maximum workload hours.
    """

    def _run(
        self,
        skill: str,
        max_workload: int
    ):
        print(f"Searching for employees with skill: {skill} and max workload: {max_workload} hours.")
        employees = employees_collection.find(
            {
                "skills": skill,
                "workload_hours": {
                    "$lte": max_workload
                },
                # "availability": True
            },
            {
                "_id": 0
            }
        )

        results = list(employees)

        if not results:
            return "No matching employees found."

        return str(results)



