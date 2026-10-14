
from crewai import Agent, LLM
# from flow_practice.crews.tools.employee_tool import EmployeeSearchTool
from crewai import Task
import os

from crewai import Agent, LLM

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

llm = LLM(
    model=f"ollama/{os.getenv('OLLAMA_MODEL', 'gpt-oss:latest')}",
    base_url=os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434",
    ),
    temperature=0.2,
)


employee_search_tool = EmployeeSearchTool()


employee_agent = Agent(
    role="Employee Search Specialist",

    goal=(
        "Correctly identify the requested employee operation and use the "
        "appropriate tool. Use create_employee for creating records "
        "employee_by_id for retrieving a specific employee, and "
        "employee_search for searching employees by skills or workload."
        "create_employee for creation, and update_employee for modification."
    ),
    backstory=(
        "You are an employee management assistant connected to MongoDB."
        "You must distinguish read operations from write operations."
        "When the user explicitly requests creating or adding an employee"
        "use create_employee. Do not use employee_search to handle a creation "
        "request. Never invent missing employee information."
        "Never use create_employee to modify an existing employee. "
        "For update requests, use update_employee and change only the "
    ),

    tools=[
        EmployeeSearchTool(),
        EmployeeByIdTool(),
        CreateEmployeeTool(),
        UpdateEmployeeTool(),
        DeleteEmployeeTool(),
    ],

    llm=llm,

    verbose=True,
)

