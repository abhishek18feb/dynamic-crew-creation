
from fastapi import APIRouter, HTTPException, status, Depends

from flow_practice.crews.database.llm_config_repository import (
    LLMConfigRepository,
)
from flow_practice.models.llm_config import LLMConfig

router = APIRouter(
    prefix="/llm-configs",
    tags=["LLM Configurations"],
)

# repository = LLMConfigRepository()
def get_llm_repository() -> LLMConfigRepository:
    return LLMConfigRepository()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_llm_config(config: LLMConfig, repository: LLMConfigRepository = Depends(get_llm_repository)):
    try:
        return repository.create(config)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get("/dropdown")
def list_chat_models_for_dropdown(repository: LLMConfigRepository = Depends(get_llm_repository)):
    return repository.list_active_chat_models()


@router.get("")
def list_all_llm_configs(repository: LLMConfigRepository = Depends(get_llm_repository)):
    return repository.list_all()


@router.get("/{llm_config_id}")
def get_llm_config(llm_config_id: str, repository: LLMConfigRepository = Depends(get_llm_repository)):
    config = repository.get_by_id(llm_config_id)

    if config is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"LLM configuration '{llm_config_id}' "
                "was not found"
            ),
        )

    return config


