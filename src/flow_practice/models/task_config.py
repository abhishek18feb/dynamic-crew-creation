
from pydantic import BaseModel, ConfigDict, Field


class TaskConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=150)

    description: str = Field(
        min_length=1,
        max_length=5000,
    )
    expected_output: str = Field(
        min_length=1,
        max_length=3000,
    )

    agent_id: str = Field(min_length=1, max_length=100)

    is_active: bool = True
    async_execution: bool = False
    human_input: bool = False
