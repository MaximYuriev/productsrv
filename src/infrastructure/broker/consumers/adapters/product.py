from src.application.dto.order import OrderDTO
from src.application.dto.product import PurchasedProductDTO
from src.application.services.product import ProductService
from src.infrastructure.broker.consumers.schemas.order import OrderBrokerSchema


class ProductBrokerAdapter:
    def __init__(self, service: ProductService):
        self._service = service

    async def purchase_product(self, order_schema: OrderBrokerSchema) -> None:
        purchased_product_list = [
            PurchasedProductDTO(**product.model_dump(by_alias=True))
            for product in order_schema.products
        ]
        order_data = order_schema.model_dump(exclude_unset=True)
        order = OrderDTO(**order_data, purchased_product_list=purchased_product_list)
        await self._service.purchase_product(order)
