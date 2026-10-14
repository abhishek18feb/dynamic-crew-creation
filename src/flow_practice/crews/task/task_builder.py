
from crewai import Task

from flow_practice.crews.agent.agent_builder import AgentBuilder
from flow_practice.crews.database.task_config_repository import (
    TaskConfigRepository,
)
from flow_practice.crews.database.mongodb import database


class TaskBuilder:
    def __init__(self):
        self.repository = TaskConfigRepository()
        self.agent_builder = AgentBuilder(database=database)

    def build_task(self, task_id: str, agent=None) -> Task:
        config = self.repository.get_by_id(task_id)

        if config is None:
            raise ValueError(
                f"Task configuration '{task_id}' was not found"
            )

        if not config.get("is_active", False):
            raise ValueError(
                f"Task configuration '{task_id}' is inactive"
            )

        # agent_id = config["agent_id"]

        # Resolve the assigned agent from MongoDB configuration.
        # agent = self.agent_builder.build_agent(agent_id)
        if agent is None:
            agent = self.agent_builder.build_agent(
                config["agent_id"]
            )

        return Task(
            name=config["name"],
            description=config["description"],
            expected_output=config["expected_output"],
            agent=agent,
            async_execution=config.get(
                "async_execution", False
            ),
            human_input=config.get("human_input", False),
        )
