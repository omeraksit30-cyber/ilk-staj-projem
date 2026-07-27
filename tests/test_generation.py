from types import SimpleNamespace

from restaurant_support_assistant.config import Settings
from restaurant_support_assistant.generation import (
    INSUFFICIENT_CONTEXT,
    answer_question,
)


def test_unrelated_question_has_insufficient_context(retriever, settings):
    result = answer_question(
        "How are spacecraft engines assembled?", retriever, settings
    )
    assert result.answer == INSUFFICIENT_CONTEXT
    assert not result.sources


def test_api_key_absent_uses_local_mode(retriever, settings):
    def forbidden_factory(**_kwargs):
        raise AssertionError("OpenAI client must not be created")

    result = answer_question(
        "What is the reservation policy?",
        retriever,
        settings,
        client_factory=forbidden_factory,
    )
    assert result.used_ai is False


def test_local_answer_includes_source_references(retriever, settings):
    result = answer_question("When are dining rooms open?", retriever, settings)
    assert result.sources
    assert "Sources: Knowledge base — Opening Hours" in result.answer


def test_mocked_ai_answer_includes_source_references(retriever):
    captured = {}

    class MockResponses:
        def create(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(output_text="Reservations require confirmation.")

    class MockClient:
        responses = MockResponses()

    def factory(**kwargs):
        captured["client_arguments"] = kwargs
        return MockClient()

    marker = "synthetic-test-value"
    settings = Settings(RETRIEVAL_TOP_K=1)
    object.__setattr__(settings, "openai_api_key", marker)
    result = answer_question(
        "How do reservations work?",
        retriever,
        settings,
        client_factory=factory,
    )
    assert result.used_ai is True
    assert "Sources: Knowledge base — Reservation Policy" in result.answer
    assert "REFERENCE CONTEXT" in captured["input"]
    assert "environment variables" in captured["instructions"]
    assert captured["client_arguments"] == {"api_key": marker}


def test_provider_failure_is_safe_and_does_not_return_secret(retriever):
    marker = "synthetic-sensitive-marker"

    def failing_factory(**_kwargs):
        raise RuntimeError(marker)

    settings = Settings(RETRIEVAL_TOP_K=1)
    object.__setattr__(settings, "openai_api_key", marker)
    result = answer_question(
        "What is the allergen process?",
        retriever,
        settings,
        client_factory=failing_factory,
    )
    assert result.used_ai is False
    assert marker not in result.answer
    assert all(marker not in source.text for source in result.sources)


def test_secret_values_are_not_logged(retriever, caplog):
    marker = "synthetic-sensitive-marker"

    def failing_factory(**_kwargs):
        raise RuntimeError(marker)

    settings = Settings()
    object.__setattr__(settings, "openai_api_key", marker)
    answer_question(
        "What menu categories exist?",
        retriever,
        settings,
        client_factory=failing_factory,
    )
    assert marker not in caplog.text
