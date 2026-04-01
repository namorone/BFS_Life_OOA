from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "BFS Life API"
    DATABASE_URL: str
    DATABASE_URL_SYNC: str
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    MEDIA_ROOT: str = "./media"
    WARRANTY_EXPIRING_DAYS: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
