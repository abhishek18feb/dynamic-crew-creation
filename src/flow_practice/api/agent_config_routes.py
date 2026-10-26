
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from flow_practice.models.agent_config import AgentConfig
from flow_practice.crews.database.agent_config_repository import (
    AgentConfigRepository,
)
from flow_practice.crews.database.llm_config_repository import (
    LLMConfigRepository,
)
from flow_practice.crews.database.mongodb import database

class AgentLLMSelection(BaseModel):
    llm_config_id: str = Field(min_length=1, max_length=100)

router = APIRouter(prefix="/agent-configs", tags=["Agent Configurations"])

def get_agent_repository() -> AgentConfigRepository:
    return AgentConfigRepository(database=database)


def get_llm_repository() -> LLMConfigRepository:
    return LLMConfigRepository()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_agent_config(config: AgentConfig, repository: AgentConfigRepository = Depends(get_agent_repository),):
    try:
        return repository.create(config)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get("/{agent_id}")
def get_agent_config(agent_id: str, repository: AgentConfigRepository = Depends(get_agent_repository),):
    config = repository.get_by_id(agent_id)

    if config is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_id}' not found",
        )

    return config


@router.get("")
def list_active_agent_configs(repository: AgentConfigRepository = Depends(get_agent_repository),):
    return repository.list_active()

@router.patch("/{agent_id}/llm-config")
def update_agent_llm(
    agent_id: str,
    selection: AgentLLMSelection,
    repository: AgentConfigRepository = Depends(get_agent_repository),
    model_repository: LLMConfigRepository = Depends(get_llm_repository),
):
    # model_repository = model_repository()
    model = model_repository.get_by_id(selection.llm_config_id)

    if (
        model is None
        or not model.get("is_active", False)
        or model.get("model_type") != "chat"
    ):
        raise HTTPException(
            status_code=400,
            detail="Select an active, configured chat model",
        )

    updated = repository.update_llm_config(
        agent_id,
        selection.llm_config_id,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{agent_id}' was not found",
        )

    return {
        "success": True,
        "agent_id": agent_id,
        "llm_config_id": selection.llm_config_id,
    }
