
from pymongo import ASCENDING
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from flow_practice.models.agent_config import AgentConfig


class AgentConfigRepository:
    def __init__(self, database):
        self.collection: Collection = database["agent_configs"]

        # A unique index prevents duplicate agent IDs.
        self.collection.create_index(
            [("agent_id", ASCENDING)],
            unique=True,
            name="unique_agent_id",
        )

    def create(self, config: AgentConfig) -> dict:
        document = config.model_dump()

        try:
            self.collection.insert_one(document)
        except DuplicateKeyError as exc:
            raise ValueError(
                f"Agent configuration '{config.agent_id}' already exists"
            ) from exc
        document.pop("_id", None)  # Remove the MongoDB-generated ID before returning
        return document

    def get_by_id(self, agent_id: str) -> dict | None:
        return self.collection.find_one(
            {"agent_id": agent_id},
            {"_id": 0},
        )

    def list_active(self) -> list[dict]:
        return list(
            self.collection.find(
                {"is_active": True},
                {"_id": 0},
            )
        )

    def update(
        self,
        agent_id: str,
        updates: dict,
    ) -> dict | None:
        allowed_fields = {
            "name",
            "role",
            "goal",
            "backstory",
            "llm_config_id",
            "tool_ids",
            "allow_delegation",
            "verbose",
            "is_active",
            "max_iter",
            # "extra_config",
        }

        if not updates or not set(updates).issubset(allowed_fields):
            raise ValueError("Invalid or empty agent configuration update")

        self.collection.update_one(
            {"agent_id": agent_id},
            {"$set": updates},
        )

        return self.get_by_id(agent_id)

    def update_llm_config(
        self,
        agent_id: str,
        llm_config_id: str,
    ) -> bool:
        result = self.collection.update_one(
            {"agent_id": agent_id},
            {"$set": {"llm_config_id": llm_config_id}},
        )

        return result.matched_count > 0
