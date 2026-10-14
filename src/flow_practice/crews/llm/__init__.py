
from crewai import LLM

from flow_practice.crews.database.llm_config_repository import (
    LLMConfigRepository,
)


class LLMRegistry:
    def __init__(self):
        self.repository = LLMConfigRepository()

    def resolve(self, llm_config_id: str) -> LLM:
        config = self.repository.get_by_id(llm_config_id)

        if config is None:
            raise ValueError(
                f"LLM configuration '{llm_config_id}' was not found"
            )

        if not config.get("is_active", False):
            raise ValueError(
                f"LLM configuration '{llm_config_id}' is inactive"
            )

        if config.get("model_type") != "chat":
            raise ValueError(
                f"LLM configuration '{llm_config_id}' "
                "is not a chat model"
            )

        if config.get("provider") != "ollama":
            raise ValueError(
                f"Unsupported LLM provider: "
                f"{config.get('provider')}"
            )

        model_name = config["model_name"]

        return LLM(
            model=f"ollama/{model_name}",
            base_url=config.get(
                "base_url",
                "http://localhost:11434",
            ),
            temperature=config.get("temperature", 0.2),
        )
