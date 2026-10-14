
from pymongo import ASCENDING
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from flow_practice.crews.database.mongodb import database
from flow_practice.models.task_config import TaskConfig


class TaskConfigRepository:
    def __init__(self):
        self.collection: Collection = database["task_configs"]

        self.collection.create_index(
            [("task_id", ASCENDING)],
            unique=True,
            name="unique_task_id",
        )

    def create(self, config: TaskConfig) -> dict:
        document = config.model_dump()

        try:
            self.collection.insert_one(document)
        except DuplicateKeyError as exc:
            raise ValueError(
                f"Task '{config.task_id}' already exists"
            ) from exc
        document.pop("_id", None)  # Remove the MongoDB-generated ID before returning
        return document

    def get_by_id(self, task_id: str) -> dict | None:
        return self.collection.find_one(
            {"task_id": task_id},
            {"_id": 0},
        )

    def list_active(self) -> list[dict]:
        return list(
            self.collection.find(
                {"is_active": True},
                {"_id": 0},
            )
        )
