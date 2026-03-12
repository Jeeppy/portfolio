from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_prefix: str = "/api"
    app_name: str = "Portfolio API"
    database_url: str = "sqlite:///./data/portfolio.db"
    debug: bool = False
    model_config = {"env_file": ".env", "extra": "ignore"}

    # Auth
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    # Admin
    admin_email: str
    admin_password: str

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
