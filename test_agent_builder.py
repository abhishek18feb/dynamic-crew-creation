from flow_practice.crews.agent.agent_builder import AgentBuilder
from flow_practice.crews.database.mongodb import database

builder = AgentBuilder(database=database)

agent = builder.build_agent("employee_researcher")

print("Agent created successfully")
print("Role:", agent.role)
print("Goal:", agent.goal)
print("Backstory:", agent.backstory)
print("Tools:", agent.tools)
print("Loaded tools:", [tool.name for tool in agent.tools])