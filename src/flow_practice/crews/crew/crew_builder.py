from crewai import Crew, Process

from flow_practice.crews.database.mongodb import database
from flow_practice.crews.agent.agent_builder import AgentBuilder
from flow_practice.crews.database.crew_config_repository import (
    CrewConfigRepository,
)
from flow_practice.crews.database.task_config_repository import (
    TaskConfigRepository,
)
from flow_practice.crews.task.task_builder import TaskBuilder


class CrewBuilder:
    def __init__(self):
        self.crew_repository = CrewConfigRepository()
        self.task_repository = TaskConfigRepository()
        self.agent_builder = AgentBuilder(database=database)
        self.task_builder = TaskBuilder()

    def build_crew(self, crew_id: str) -> Crew:
        config = self.crew_repository.get_by_id(crew_id)

        if config is None:
            raise ValueError(
                f"Crew configuration '{crew_id}' was not found"
            )

        if not config.get("is_active", False):
            raise ValueError(
                f"Crew configuration '{crew_id}' is inactive"
            )

        task_ids = config["task_ids"]

        agents_by_id = {}
        tasks = []

        for task_id in task_ids:
            task_config = self.task_repository.get_by_id(task_id)

            if task_config is None:
                raise ValueError(
                    f"Task configuration '{task_id}' was not found"
                )

            if not task_config.get("is_active", False):
                raise ValueError(
                    f"Task configuration '{task_id}' is inactive"
                )

            agent_id = task_config["agent_id"]

            if agent_id not in agents_by_id:
                agents_by_id[agent_id] = (
                    self.agent_builder.build_agent(agent_id)
                )

            task = self.task_builder.build_task(
                task_id,
                agent=agents_by_id[agent_id],
            )
            tasks.append(task)

        agents = list(agents_by_id.values())

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=config.get("verbose", True),
        )
