
import pytest
from pydantic import ValidationError

from flow_practice.models.agent_config import AgentConfig


@pytest.fixture
def valid_agent_config():
    return {
        "agent_id": "employee_researcher",
        "name": "Employee Researcher",
        "role": "Employee Research Specialist",
        "goal": "Find employees matching the requested skills",
        "backstory": "You analyze employee skills and availability.",
        "llm_config_id": "ollama_gpt_oss",
        "tool_ids": ["employee_search", "employee_by_id"],
        "allow_delegation": False,
        "verbose": True,
        "is_active": True,
        "max_iter": 10,
    }


def test_valid_agent_config(valid_agent_config):
    config = AgentConfig(**valid_agent_config)

    assert config.agent_id == "employee_researcher"
    assert config.llm_config_id == "ollama_gpt_oss"
    assert config.is_active is True


def test_agent_config_requires_agent_id(valid_agent_config):
    valid_agent_config.pop("agent_id")

    with pytest.raises(ValidationError):
        AgentConfig(**valid_agent_config)


def test_agent_config_rejects_unknown_fields(valid_agent_config):
    valid_agent_config["unexpected_field"] = "not allowed"

    with pytest.raises(ValidationError):
        AgentConfig(**valid_agent_config)


def test_agent_max_iter_must_be_valid(valid_agent_config):
    valid_agent_config["max_iter"] = 0

    with pytest.raises(ValidationError):
        AgentConfig(**valid_agent_config)
