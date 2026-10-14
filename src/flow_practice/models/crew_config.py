from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CrewConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    crew_id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=150)

    description: str = Field(
        default="",
        max_length=1000,
    )

    task_ids: list[str] = Field(min_length=1)

    process: Literal["sequential"] = "sequential"
    is_active: bool = True
    verbose: bool = True

    @model_validator(mode="after")
    def validate_task_ids(self):
        if len(self.task_ids) != len(set(self.task_ids)):
            raise ValueError(
                "task_ids must not contain duplicate IDs"
            )
        return self
