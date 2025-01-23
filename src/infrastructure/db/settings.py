from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import PostgresConfig


def create_async_session_maker(db_config: PostgresConfig):
    db_engine = create_async_engine(db_config.db_url, echo=False)
    return async_sessionmaker(db_engine, expire_on_commit=False)
