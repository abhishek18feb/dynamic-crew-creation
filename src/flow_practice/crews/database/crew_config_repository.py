from pymongo import ASCENDING
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from flow_practice.crews.database.mongodb import database
from flow_practice.models.crew_config import CrewConfig


class CrewConfigRepository:
    def __init__(self):
        self.collection: Collection = database["crew_configs"]

        self.collection.create_index(
            [("crew_id", ASCENDING)],
            unique=True,
            name="unique_crew_id",
        )

    def create(self, config: CrewConfig) -> dict:
        document = config.model_dump()

        try:
            self.collection.insert_one(document)
        except DuplicateKeyError as exc:
            raise ValueError(
                f"Crew '{config.crew_id}' already exists"
            ) from exc
        document.pop("_id", None)  # Remove the MongoDB ObjectId before returning
        return document

    def get_by_id(self, crew_id: str) -> dict | None:
        return self.collection.find_one(
            {"crew_id": crew_id},
            {"_id": 0},
        )

    def list_active(self) -> list[dict]:
        return list(
            self.collection.find(
                {"is_active": True},
                {"_id": 0},
            )
        )
