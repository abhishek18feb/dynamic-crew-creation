from pydantic import BaseModel


class Employee(BaseModel):
    employee_id: str
    name: str
    role: str
    email: str
    skills: list[str]
    resume_path: str
    experience_years: int
    workload_hours: int