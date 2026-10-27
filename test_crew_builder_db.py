
from flow_practice.crews.crew.crew_builder import CrewBuilder


builder = CrewBuilder()

crew = builder.build_crew("employee_management_crew")

print("Crew built successfully")
print("Agents:")

for agent in crew.agents:
    print("-", agent.role)

print("Tasks:")

for task in crew.tasks:
    print("-", task.name)
    print("  Assigned agent:", task.agent.role)
