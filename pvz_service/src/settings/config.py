from datetime import timedelta
from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    INTERNAL_API_KEY: str

    inbox_stale_timeout_seconds: int = 30

    @cached_property
    def inbox_stale_timeout(self) -> timedelta:
        return timedelta(seconds=self.inbox_stale_timeout_seconds)

    model_config = SettingsConfigDict(env_file=".env")

    def CONNECT_ASYNC(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
