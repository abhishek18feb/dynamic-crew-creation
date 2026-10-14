from crewai import Crew, Process, Task

from flow_practice.crews.agent.employee_agent import (
    employee_agent,
    # employee_task,
)

def create_employee_crew(query: str):

    employee_task = Task(
        description=f"""
            Perform the employee operation described in this request:

            {query}

            Select the appropriate tool:
            - Create or add an employee: create_employee
            - Retrieve one employee by ID: employee_by_id
            - Search employees by skills or workload: employee_search
            - resume_path is optional. 
            - If the user does not provide it use an empty string.
            - If the user explicitly requests changing or modifying an existing employee, use update_employee. 
            - Do not use create_employee for update requests.
            - Do not overwrite fields that the user did not request to change.
            - If the user requests deleting an employee, use delete_employee.
            - Deletion requires explicit confirmation for the exact employee ID.
            - Do not treat a request to look up an employee as confirmation to delete.
            - Never delete an employee if confirmation is missing or false.

            The request above is the user's actual request.
            Do not ask the user to provide it again.
        """,

        expected_output="""
        The employee records returned by the employee_search
        tool in JSON-compatible format.
        """,

        agent=employee_agent,
    )

    crew = Crew(
        agents=[
            employee_agent
        ],

        tasks=[
            employee_task
        ],

        process=Process.sequential,

        verbose=True,
    )

    return crew

# crew = create_employee_crew(query=q)

# def kickoff():
#     result = crew.kickoff()
#     print(result.raw)

# if __name__ == "__main__":
#     kickoff()