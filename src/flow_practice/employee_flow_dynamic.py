from flow_practice.crews.crew.crew_builder import CrewBuilder


class EmployeeFlowDynamic:
    def __init__(self):
        self.crew_builder = CrewBuilder()

    def kickoff(self, inputs: dict):
        query = inputs.get("query")

        if not isinstance(query, str) or not query.strip():
            raise ValueError("A non-empty employee query is required")

        crew = self.crew_builder.build_crew(
            "employee_management_crew"
        )

        return crew.kickoff(
            inputs={"query": query.strip()}
        )
