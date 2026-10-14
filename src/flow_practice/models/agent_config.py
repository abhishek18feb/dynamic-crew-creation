
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AgentConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent_id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=150)
    role: str = Field(min_length=1, max_length=300)
    goal: str = Field(min_length=1, max_length=1000)
    backstory: str = Field(min_length=1, max_length=2000)

    llm_config_id: str = "local_ollama"
    tool_ids: list[str] = Field(default_factory=list)

    allow_delegation: bool = False
    verbose: bool = True
    is_active: bool = True

    # Optional, explicitly approved agent settings
    max_iter: int = Field(default=10, ge=1, le=50)
    # extra_config: dict[str, Any] = Field(default_factory=dict)
