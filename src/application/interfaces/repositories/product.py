from abc import ABC, abstractmethod

from src.domain.models.product import Product


class IProductRepository(ABC):
    @abstractmethod
    async def add(self, product: Product) -> None: ...

    @abstractmethod
    async def get_product_by_name(self, product_name: str) -> Product: ...

    @abstractmethod
    async def get_product_by_id(self, product_id: int) -> Product: ...

    @abstractmethod
    async def get_products(self, offset: int, limit: int, **kwargs) -> list[Product]: ...
