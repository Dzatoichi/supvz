from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Класс конфига для работы с БД.
    """

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    LOG_LEVEL: str
    LOG_TO_CONSOLE: bool
    LOGS_DIR: str

    model_config = SettingsConfigDict(env_file=".env")

    def CONNECT_ASYNC(self):
        """
        Функция создания соединения с БД.
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
