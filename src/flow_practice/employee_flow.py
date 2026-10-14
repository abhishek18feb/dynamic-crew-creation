from typing import Any

from pydantic import BaseModel, Field

from crewai import Crew, Process, Task
from crewai.flow import Flow, start

# from flow_practice.crews.agent.employee_agent import (
#     employee_agent,
# )

from flow_practice.employee_crew import (
    create_employee_crew,
)

# from flow_practice.crews.database.employee_repository import (
#     search_employees,
# )

from pydantic import BaseModel
# from flow_practice.models.employee import Employee

class EmployeeState(BaseModel):

    query: str = ""

    result: Any = None


class EmployeeFlow(Flow[EmployeeState]):

    @start()
    def search_employees(self):

        crew = create_employee_crew(
            query=self.state.query
        )

        result = crew.kickoff()

        self.state.result = result

        return result