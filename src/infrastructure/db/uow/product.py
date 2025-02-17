from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.interfaces.uow.product import IProductUoW
from src.infrastructure.db.repositories.product import ProductRepository


class ProductUoW(IProductUoW):
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self._session_maker = session_maker

    async def __aenter__(self) -> None:
        self._session = self._session_maker()
        self._product_repository = ProductRepository(self._session)

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._session.rollback()
        await self._session.close()

    @property
    def product_repository(self) -> ProductRepository:
        return self._product_repository

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
