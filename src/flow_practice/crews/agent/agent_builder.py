from crewai import Agent

from flow_practice.crews.database.agent_config_repository import (
    AgentConfigRepository,
)
from flow_practice.crews.tools.tool_registry import resolve_tools
from flow_practice.crews.llm.llm_registry import LLMRegistry

class AgentBuilder:
    def __init__(self, database):
        self.repository = AgentConfigRepository(database=database)
        self.llm_registry = LLMRegistry()
    def build_agent(self, agent_id: str) -> Agent:
        config = self.repository.get_by_id(agent_id)

        if config is None:
            raise ValueError(
                f"Agent configuration '{agent_id}' was not found"
            )

        if not config.get("is_active", False):
            raise ValueError(
                f"Agent configuration '{agent_id}' is inactive"
            )

        # Tool resolution will be added in the next step.
        # For now, construct an agent without tools.
        

        llm_config_id = config.get("llm_config_id")

        if not llm_config_id:
            raise ValueError(
                f"Agent '{agent_id}' has no llm_config_id"
            )

        llm = self.llm_registry.resolve(llm_config_id)
        tools = resolve_tools(config.get("tool_ids", []))
        
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            tools=tools,
            llm=llm,
            # allow_delegation=config["allow_delegation"],
            allow_delegation=config.get(
                "allow_delegation", False
            ),
            verbose=config.get("verbose", True),
            max_iter=config.get("max_iter", 10),
        )