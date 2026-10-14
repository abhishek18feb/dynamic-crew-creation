
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LLMConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    llm_config_id: str = Field(
        min_length=1,
        max_length=100,
    )
    name: str = Field(
        min_length=1,
        max_length=150,
    )

    provider: Literal["ollama"] = "ollama"
    model_name: str = Field(
        min_length=1,
        max_length=200,
    )

    model_type: Literal["chat", "embedding"] = "chat"

    base_url: str = "http://localhost:11434"

    temperature: float = Field(default=0.2, ge=0, le=2)
    is_active: bool = True
