from typing import AsyncGenerator, AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.adapters.product import FromRouterToProductServiceAdapter
from src.application.interfaces.repositories.product import IProductRepository
from src.application.services.product import ProductService
from src.infrastructure.db.repositories.product import ProductRepository
from src.infrastructure.db.settings import async_session_maker


class AppProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_session(self) -> AsyncIterable[AsyncSession]:
        async with async_session_maker() as session:
            yield session

    product_repository = provide(ProductRepository, scope=Scope.REQUEST, provides=IProductRepository)
    product_service = provide(ProductService, scope=Scope.REQUEST)
    product_adapter = provide(FromRouterToProductServiceAdapter, scope=Scope.REQUEST)
