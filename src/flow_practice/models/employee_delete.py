from pydantic import BaseModel, Field


class EmployeeDeleteInput(BaseModel):
    employee_id: str = Field(min_length=1)
    confirm_delete: bool = False