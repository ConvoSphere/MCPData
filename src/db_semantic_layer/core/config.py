from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
	model_config = SettingsConfigDict(env_file=".env", env_prefix="DBSL_", case_sensitive=False)

	default_connection: str | None = Field(default=None, description="Name der Default-Verbindung")
	telemetry_enabled: bool = Field(default=False)
	otel_endpoint: str | None = Field(default=None, description="OTLP Endpoint")
	llm_model: str = Field(default="gpt-4o-mini", description="litellm Modellname")
	embedding_model: str = Field(default="text-embedding-3-small", description="litellm Embedding-Modell")


settings = AppSettings()