
from flow_practice.crews.task.task_builder import TaskBuilder


builder = TaskBuilder()

task = builder.build_task("employee_search_task")

print("Task name:", task.name)
print("Task description:", task.description)
print("Expected output:", task.expected_output)
print("Assigned agent:", task.agent.role)
print(
    "Agent tools:",
    [tool.name for tool in task.agent.tools],
)
