from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str  # type annotation only, no inline value
    ALEMBIC_DATABASE_URL: str | None = None  # ← optional for runtime


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
