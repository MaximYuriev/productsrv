from abc import ABC, abstractmethod

from src.domain.models.product import Product


class IProductRepository(ABC):
    @abstractmethod
    async def add(self, product: Product) -> None: ...

    @abstractmethod
    async def get_product_by_name(self, product_name: str) -> Product: ...