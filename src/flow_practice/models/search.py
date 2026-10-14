from pydantic import BaseModel, Field


class EmployeeSearchCriteria(BaseModel):
    skills: list[str] = Field(
        description="Skills that the employee should have"
    )

    max_workload: int = Field(
        description="Maximum allowed workload hours"
    )