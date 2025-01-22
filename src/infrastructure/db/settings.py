from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import config

db_engine = create_async_engine(config.db.url, echo=False)
async_session_maker = async_sessionmaker(db_engine, expire_on_commit=False)


async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
