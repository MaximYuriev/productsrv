from abc import ABC, abstractmethod

from src.domain.models.product import Product


class IProductPublisher(ABC):
    _EXCHANGE = "product"
    _CREATE_PRODUCT_QUEUE = "product-create"
    _UPDATE_PRODUCT_QUEUE = "product-update"
    _DELETE_PRODUCT_QUEUE = "product-delete"

    @abstractmethod
    async def publish_create_product(self, product: Product) -> None:
        pass

    @abstractmethod
    async def publish_update_product(self, product: Product) -> None:
        pass

    @abstractmethod
    async def publish_delete_product(self, product: Product) -> None:
        pass
