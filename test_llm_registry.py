
from flow_practice.crews.llm.llm_registry import LLMRegistry
from flow_practice.crews.agent.agent_builder import AgentBuilder
from flow_practice.crews.database.mongodb import database

registry = LLMRegistry()

llm = registry.resolve("ollama_gpt_oss")
print("LLM object created:", type(llm).__name__)

builder = AgentBuilder(database=database)
agent = builder.build_agent("employee_researcher")

print("Agent:", agent.role)
print("Agent tools:", [tool.name for tool in agent.tools])
print("Agent built with configured LLM.")
