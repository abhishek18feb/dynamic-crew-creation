from typing import Type

from pydantic import BaseModel, Field

from crewai.tools import BaseTool


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""

    argument: str = Field(..., description="Description of the argument.")

class EmployeeSearchInput(BaseModel):
    skill: str = Field(
        ...,
        description="Skill to search for, such as Python or React"
    )

    max_workload: int = Field(
        ...,
        description="Maximum workload hours"
    )

class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = "Clear description for what this tool is useful for, your agent will need this information to use it."
    args_schema: Type[BaseModel] = EmployeeSearchInput

    def _run(self, argument: str) -> str:
        return "this is an example of a tool output, ignore it and move along."
