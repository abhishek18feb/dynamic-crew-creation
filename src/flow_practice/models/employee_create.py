from pydantic import BaseModel, EmailStr, Field


class EmployeeCreateInput(BaseModel):
    employee_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    role: str = Field(min_length=1)
    email: EmailStr
    skills: list[str] = Field(min_length=1)
    # resume_path: str = ""
    experience_years: int = Field(ge=0)
    workload_hours: int = Field(ge=0)