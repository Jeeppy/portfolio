from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_prefix: str = "/api"
    app_name: str = "Portfolio API"
    debug: bool = False

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
