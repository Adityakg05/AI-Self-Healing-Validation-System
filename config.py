"""AI-Self-Healing-Validation-System configuration with validation.

Import `settings` instead of using os.getenv() directly.

Usage:
    from config import settings
    llm_provider = settings.llm_provider
"""
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # LLM
    llm_provider: str = "groq"  # "groq" | "gemini"

    # Groq
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    # Gemini
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"

    # GitHub
    github_token: str = ""
    github_repo: str = ""
    github_branch: str = "main"

    # App
    app_port: int = 8000
    log_file: str = "app_logs.txt"
    max_iterations: int = 3

    # LangSmith
    langchain_tracing_v2: bool = False
    langchain_api_key: str = ""
    langchain_project: str = "sre-agent"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_llm_keys(self) -> "Settings":
        # Ensure valid LLM provider is set
        if self.llm_provider not in ("groq", "gemini"):
            raise ValueError(
                f"LLM_PROVIDER must be 'groq' or 'gemini', got: {self.llm_provider!r}"
            )
        if self.llm_provider == "groq" and not self.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY is required when LLM_PROVIDER=groq."
            )
        if self.llm_provider == "gemini" and not self.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is required when LLM_PROVIDER=gemini."
            )
        return self


settings = Settings()
