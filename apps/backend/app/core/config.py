from __future__ import annotations

from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "BFS Life API"
    DATABASE_URL: str
    DATABASE_URL_SYNC: str
    SECRET_KEY: str = "dev-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    MEDIA_ROOT: str = "./media"
    WARRANTY_EXPIRING_DAYS: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class PytestDatabaseSettings(BaseSettings):
    """Тестова БД для pytest: дефолти під docker-compose.

    Перевизначення — змінні TEST_* у env / .env.
    """

    TEST_DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@db:5432/bfs_test",
    )
    TEST_DATABASE_URL_SYNC: str | None = Field(default=None)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


_settings_instance: Settings | None = None


def get_settings() -> Settings:
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance


def apply_pytest_database_environ() -> None:
    """Викликати з tests/conftest до import app.

    Будує один екземпляр Settings з URL з PytestDatabaseSettings.
    """
    global _settings_instance
    cfg = PytestDatabaseSettings()
    async_url = cfg.TEST_DATABASE_URL.strip()
    sync_url = cfg.TEST_DATABASE_URL_SYNC
    if sync_url is None:
        sync_url = async_url.replace("postgresql+asyncpg://", "postgresql://", 1)
    sync_url = sync_url.strip()
    # Решта полів (SECRET_KEY тощо) — з env / .env, як у prod.
    _settings_instance = Settings(
        DATABASE_URL=async_url,
        DATABASE_URL_SYNC=sync_url,
    )


class _SettingsProxy:
    __slots__ = ()

    def __getattr__(self, name: str) -> Any:
        return getattr(get_settings(), name)


settings = _SettingsProxy()
