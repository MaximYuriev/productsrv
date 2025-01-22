from pydantic import Field
from pydantic_settings import BaseSettings

from config.db import DataBaseConfig


class Config(BaseSettings):
    db: DataBaseConfig = Field(default_factory=DataBaseConfig)


config = Config()
