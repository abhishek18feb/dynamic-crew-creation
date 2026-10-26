
from fastapi import APIRouter, HTTPException, status, Depends

from flow_practice.crews.database.task_config_repository import (
    TaskConfigRepository,
)
from flow_practice.models.task_config import TaskConfig


router = APIRouter(
    prefix="/task-configs",
    tags=["Task Configurations"],
)

# repository = TaskConfigRepository()
def get_task_repository() -> TaskConfigRepository:
    return TaskConfigRepository()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task_config(config: TaskConfig, repository: TaskConfigRepository = Depends(get_task_repository)):
    try:
        return repository.create(config)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get("/{task_id}")
def get_task_config(task_id: str, repository: TaskConfigRepository = Depends(get_task_repository)):
    config = repository.get_by_id(task_id)

    if config is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task configuration '{task_id}' was not found",
        )

    return config


@router.get("")
def list_task_configs(repository: TaskConfigRepository = Depends(get_task_repository)):
    return repository.list_active()
