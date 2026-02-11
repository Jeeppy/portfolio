from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_prefix: str = "/api"
    app_name: str = "Portfolio API"
    database_url: str = "sqlite:///./data/portfolio.db"
    debug: bool = False
    model_config = {"env_file": ".env", "extra": "ignore"}

    # Auth
    secret_key: str = "change-me-to-a-random-string-64-chars"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    # Admin
    admin_email: str = "admin@example.com"
    admin_password: str = "changeme"


@lru_cache
def get_settings() -> Settings:
    return Settings()
