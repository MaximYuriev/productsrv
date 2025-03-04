import uuid
from abc import ABC, abstractmethod

from src.application.dto.order import OrderDTO
from src.domain.models.product import Product


class IProductPublisher(ABC):
    @abstractmethod
    async def publish_create_product(self, product: Product) -> None:
        pass

    @abstractmethod
    async def publish_update_product(self, product: Product) -> None:
        pass

    @abstractmethod
    async def publish_delete_product(self, product: Product) -> None:
        pass

    @abstractmethod
    async def cancel_order(self, order_id: uuid.UUID, reason: str) -> None:
        pass

    @abstractmethod
    async def accept_order(self, order: OrderDTO) -> None:
        pass

    @abstractmethod
    async def clear_basket(self, order: OrderDTO) -> None:
        pass
