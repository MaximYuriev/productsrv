from typing import AsyncIterable

from dishka import Provider, Scope, provide, from_context
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.api.adapters.product import FromRouterToProductServiceAdapter
from src.application.interfaces.repositories.product import IProductRepository
from src.application.services.product import ProductService
from src.config import Config
from src.infrastructure.db.repositories.product import ProductRepository
from src.infrastructure.db.settings import create_async_session_maker


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_async_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return create_async_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    product_repository = provide(ProductRepository, scope=Scope.REQUEST, provides=IProductRepository)
    product_service = provide(ProductService, scope=Scope.REQUEST)
    product_adapter = provide(FromRouterToProductServiceAdapter, scope=Scope.REQUEST)
