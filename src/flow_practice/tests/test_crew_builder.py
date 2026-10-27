
import pytest

from flow_practice.crews.crew import crew_builder as module
from flow_practice.crews.crew.crew_builder import CrewBuilder


class FakeCrewRepository:
    def __init__(self, config=None):
        self.config = config

    def get_by_id(self, crew_id):
        return self.config


class FakeTaskRepository:
    def __init__(self, tasks=None):
        self.tasks = tasks or {}

    def get_by_id(self, task_id):
        return self.tasks.get(task_id)


class FakeAgentBuilder:
    def __init__(self, error=None):
        self.error = error
        self.built_agent_ids = []

    def build_agent(self, agent_id):
        if self.error:
            raise self.error

        self.built_agent_ids.append(agent_id)
        return f"agent:{agent_id}"


class FakeTaskBuilder:
    def build_task(self, task_id, agent):
        return {
            "task_id": task_id,
            "agent": agent,
        }


class FakeCrew:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


@pytest.fixture
def make_builder(monkeypatch):
    def factory(crew_config=None, tasks=None, agent_error=None):
        crew_repository = FakeCrewRepository(crew_config)
        task_repository = FakeTaskRepository(tasks)
        agent_builder = FakeAgentBuilder(agent_error)

        monkeypatch.setattr(
            module, "CrewConfigRepository",
            lambda: crew_repository,
        )
        monkeypatch.setattr(
            module, "TaskConfigRepository",
            lambda: task_repository,
        )
        monkeypatch.setattr(
            module, "AgentBuilder",
            lambda database: agent_builder,
        )
        monkeypatch.setattr(
            module, "TaskBuilder",
            FakeTaskBuilder,
        )
        monkeypatch.setattr(module, "Crew", FakeCrew)

        builder = CrewBuilder()

        return builder, agent_builder

    return factory


def test_build_missing_crew_raises_value_error(make_builder):
    builder, _ = make_builder(crew_config=None)

    with pytest.raises(ValueError, match="was not found"):
        builder.build_crew("unknown-crew")


def test_build_inactive_crew_raises_value_error(make_builder):
    builder, _ = make_builder(
        crew_config={
            "is_active": False,
            "task_ids": ["task-1"],
        }
    )

    with pytest.raises(ValueError, match="is inactive"):
        builder.build_crew("inactive-crew")


def test_build_missing_task_raises_value_error(make_builder):
    builder, _ = make_builder(
        crew_config={
            "is_active": True,
            "task_ids": ["missing-task"],
        },
        tasks={},
    )

    with pytest.raises(ValueError, match="was not found"):
        builder.build_crew("crew-1")


def test_build_inactive_task_raises_value_error(make_builder):
    builder, _ = make_builder(
        crew_config={
            "is_active": True,
            "task_ids": ["task-1"],
        },
        tasks={
            "task-1": {
                "is_active": False,
                "agent_id": "agent-1",
            }
        },
    )

    with pytest.raises(ValueError, match="is inactive"):
        builder.build_crew("crew-1")


def test_build_crew_reuses_agent_for_multiple_tasks(make_builder):
    builder, agent_builder = make_builder(
        crew_config={
            "is_active": True,
            "task_ids": ["task-1", "task-2"],
            "verbose": False,
        },
        tasks={
            "task-1": {
                "is_active": True,
                "agent_id": "agent-1",
            },
            "task-2": {
                "is_active": True,
                "agent_id": "agent-1",
            },
        },
    )

    crew = builder.build_crew("crew-1")

    assert len(crew.kwargs["agents"]) == 1
    assert len(crew.kwargs["tasks"]) == 2
    assert agent_builder.built_agent_ids == ["agent-1"]
    assert crew.kwargs["verbose"] is False


def test_build_crew_propagates_invalid_agent_error(make_builder):
    builder, _ = make_builder(
        crew_config={
            "is_active": True,
            "task_ids": ["task-1"],
        },
        tasks={
            "task-1": {
                "is_active": True,
                "agent_id": "unknown-agent",
            }
        },
        agent_error=ValueError("Agent configuration not found"),
    )

    with pytest.raises(ValueError, match="Agent configuration not found"):
        builder.build_crew("crew-1")
