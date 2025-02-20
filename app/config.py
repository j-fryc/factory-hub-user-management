from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str
    auth0_url: str
    auth0_client_id: str
    auth0_client_secret: str

    model_config = SettingsConfigDict(env_file="../../.env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
