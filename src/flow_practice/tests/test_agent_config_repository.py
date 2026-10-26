import mongomock
import pytest

from flow_practice.crews.database.agent_config_repository import (
    AgentConfigRepository,
)
from flow_practice.models.agent_config import AgentConfig


@pytest.fixture
def repository():
    client = mongomock.MongoClient()
    database = client["test_employee_db"]

    return AgentConfigRepository(database=database)


@pytest.fixture
def valid_agent_config():
    return AgentConfig(
        agent_id="employee_researcher",
        name="Employee Researcher",
        role="Employee Research Specialist",
        goal="Find employees matching requested skills",
        backstory="You analyze employee skills and availability.",
        llm_config_id="ollama_gpt_oss",
        tool_ids=["employee_search", "employee_by_id"],
        allow_delegation=False,
        verbose=True,
        is_active=True,
        max_iter=10,
    )


def test_create_agent_config(repository, valid_agent_config):
    created = repository.create(valid_agent_config)

    assert created["agent_id"] == "employee_researcher"

    saved = repository.get_by_id("employee_researcher")
    assert saved is not None
    assert saved["name"] == "Employee Researcher"


def test_get_nonexistent_agent_returns_none(repository):
    result = repository.get_by_id("missing_agent")

    assert result is None


def test_duplicate_agent_id_is_rejected(
    repository,
    valid_agent_config,
):
    repository.create(valid_agent_config)

    with pytest.raises(ValueError, match="already exists"):
        repository.create(valid_agent_config)


def test_update_agent_config(repository, valid_agent_config):
    repository.create(valid_agent_config)

    updated = repository.update(
        "employee_researcher",
        {"name": "Updated Employee Researcher"},
    )

    assert updated is not None
    assert updated["name"] == "Updated Employee Researcher"


def test_update_rejects_invalid_fields(repository, valid_agent_config):
    repository.create(valid_agent_config)

    with pytest.raises(ValueError, match="Invalid or empty"):
        repository.update(
            "employee_researcher",
            {"unexpected_field": "not allowed"},
        )


def test_update_nonexistent_agent_returns_none(repository):
    updated = repository.update(
        "missing_agent",
        {"name": "Updated Name"},
    )

    assert updated is None

