"""Typed environment-based application configuration."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration with bounded, safe defaults."""

    model_config = SettingsConfigDict(
        env_file=None,
        extra="ignore",
        case_sensitive=True,
    )

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_MODEL")
    retrieval_top_k: int = Field(default=3, ge=1, le=5, alias="RETRIEVAL_TOP_K")
    max_question_length: int = Field(
        default=500, ge=50, le=2_000, alias="MAX_QUESTION_LENGTH"
    )
    app_environment: str = Field(default="development", alias="APP_ENVIRONMENT")
    max_knowledge_base_bytes: int = Field(default=100_000, ge=1_000, le=1_000_000)
    max_chunk_length: int = Field(default=1_500, ge=200, le=5_000)
    minimum_relevance_score: float = Field(default=0.12, ge=0.0, le=1.0)

    @property
    def ai_enabled(self) -> bool:
        return bool(self.openai_api_key and self.openai_api_key.strip())
