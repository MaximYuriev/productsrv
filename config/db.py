from pydantic_settings import SettingsConfigDict

from config.base import BaseConfig


class DataBaseConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="db_")
    host: str
    port: str
    name: str
    user: str
    password: str

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
