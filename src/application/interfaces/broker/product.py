from abc import ABC, abstractmethod

from src.domain.models.product import Product


class IProductPublisher(ABC):
    _EXCHANGE_NAME = "product"
    _CREATE_PRODUCT_QUEUE_NAME = "product-create"
    _UPDATE_PRODUCT_QUEUE_NAME = "product-update"
    _DELETE_PRODUCT_QUEUE_NAME = "product-delete"

    @abstractmethod
    async def publish_create_product(self, product: Product) -> None:
        pass

    @abstractmethod
    async def publish_update_product(self, product: Product) -> None:
        pass

    @abstractmethod
    async def publish_delete_product(self, product: Product) -> None:
        pass
