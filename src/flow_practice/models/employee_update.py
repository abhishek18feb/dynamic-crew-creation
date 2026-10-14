from pydantic import BaseModel, EmailStr, Field


class EmployeeUpdateInput(BaseModel):
    employee_id: str = Field(min_length=1)

    name: str | None = None
    role: str | None = None
    email: EmailStr | None = None
    skills: list[str] | None = Field(default=None, min_length=1)
    resume_path: str | None = None
    experience_years: int | None = Field(default=None, ge=0)
    workload_hours: int | None = Field(default=None, ge=0)