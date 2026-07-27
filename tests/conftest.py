from pathlib import Path

import pytest

from restaurant_support_assistant.config import Settings
from restaurant_support_assistant.knowledge import load_knowledge_base
from restaurant_support_assistant.retrieval import TfidfRetriever


@pytest.fixture
def settings() -> Settings:
    return Settings(
        OPENAI_API_KEY=None,
        RETRIEVAL_TOP_K=3,
        MAX_QUESTION_LENGTH=500,
    )


@pytest.fixture
def knowledge_path() -> Path:
    return Path(__file__).parents[1] / "data" / "knowledge_base.md"


@pytest.fixture
def chunks(knowledge_path: Path):
    return load_knowledge_base(
        knowledge_path, max_file_size=100_000, max_chunk_length=1_500
    )


@pytest.fixture
def retriever(chunks):
    return TfidfRetriever(chunks)
