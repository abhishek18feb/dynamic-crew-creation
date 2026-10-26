
from pymongo import ASCENDING
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from flow_practice.crews.database.mongodb import database
from flow_practice.models.llm_config import LLMConfig


class LLMConfigRepository:
    def __init__(self, database_override=None):
        db = (
            database
            if database_override is None
            else database_override
        )

        self.collection: Collection = db["llm_configs"]

        self.collection.create_index(
            [("llm_config_id", ASCENDING)],
            unique=True,
            name="unique_llm_config_id",
        )

    def create(self, config: LLMConfig) -> dict:
        document = config.model_dump()

        try:
            self.collection.insert_one(document)
        except DuplicateKeyError as exc:
            raise ValueError(
                f"LLM configuration "
                f"'{config.llm_config_id}' already exists"
            ) from exc
        document.pop("_id", None)  # Remove the MongoDB ObjectId before returning
        return document

    def get_by_id(self, llm_config_id: str) -> dict | None:
        return self.collection.find_one(
            {"llm_config_id": llm_config_id},
            {"_id": 0},
        )

    def list_active_chat_models(self) -> list[dict]:
        return list(
            self.collection.find(
                {
                    "is_active": True,
                    "model_type": "chat",
                },
                {"_id": 0},
            ).sort("name", ASCENDING)
        )

    def list_all(self) -> list[dict]:
        return list(
            self.collection.find({}, {"_id": 0}).sort(
                "name", ASCENDING
            )
        )

