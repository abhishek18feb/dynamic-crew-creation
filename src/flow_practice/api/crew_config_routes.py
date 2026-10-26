
from fastapi import APIRouter, HTTPException, status, Depends

from flow_practice.crews.database.crew_config_repository import (
    CrewConfigRepository,
)
from flow_practice.models.crew_config import CrewConfig


router = APIRouter(
    prefix="/crew-configs",
    tags=["Crew Configurations"],
)

# repository = CrewConfigRepository()
def get_crew_repository() -> CrewConfigRepository:
    return CrewConfigRepository()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_crew_config(config: CrewConfig, repository: CrewConfigRepository = Depends(get_crew_repository)):
    try:
        return repository.create(config)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get("/{crew_id}")
def get_crew_config(crew_id: str, repository: CrewConfigRepository = Depends(get_crew_repository)):
    config = repository.get_by_id(crew_id)

    if config is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Crew configuration '{crew_id}' was not found",
        )

    return config


@router.get("")
def list_crew_configs(repository: CrewConfigRepository = Depends(get_crew_repository)):
    return repository.list_active()
