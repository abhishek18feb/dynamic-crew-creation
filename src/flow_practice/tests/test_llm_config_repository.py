
import mongomock
import pytest

from flow_practice.crews.database.llm_config_repository import (
    LLMConfigRepository,
)
from flow_practice.models.llm_config import LLMConfig


@pytest.fixture
def repository():
    client = mongomock.MongoClient()
    database = client["test_llm_db"]

    return LLMConfigRepository(database_override=database)


@pytest.fixture
def chat_model():
    return LLMConfig(
        llm_config_id="ollama_test_model",
        name="Test Ollama Model",
        provider="ollama",
        model_name="llama3.2:3b",
        model_type="chat",
        base_url="http://localhost:11434",
        temperature=0.2,
        is_active=True,
    )


def test_create_and_get_llm_config(repository, chat_model):
    repository.create(chat_model)

    saved = repository.get_by_id("ollama_test_model")

    assert saved is not None
    assert saved["model_name"] == "llama3.2:3b"
    assert saved["model_type"] == "chat"


def test_duplicate_llm_config_is_rejected(repository, chat_model):
    repository.create(chat_model)

    with pytest.raises(ValueError):
        repository.create(chat_model)


def test_get_missing_llm_config_returns_none(repository):
    result = repository.get_by_id("missing_model")

    assert result is None


def test_list_active_chat_models(repository, chat_model):
    repository.create(chat_model)

    embedding_model = LLMConfig(
        llm_config_id="ollama_test_embedding",
        name="Test Embedding Model",
        provider="ollama",
        model_name="qwen3-embedding:0.6b",
        model_type="embedding",
        is_active=True,
    )
    repository.create(embedding_model)

    models = repository.list_active_chat_models()

    assert len(models) == 1
    assert models[0]["llm_config_id"] == "ollama_test_model"
