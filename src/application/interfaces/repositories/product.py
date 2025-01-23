from abc import ABC, abstractmethod

from src.domain.models.product import Product


class IProductRepository(ABC):
    @abstractmethod
    async def add(self, product: Product) -> None: ...
