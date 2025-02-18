from dishka.integrations.faststream import inject, FromDishka
from faststream.rabbit import RabbitRouter

from src.infrastructure.broker.consumers.adapters.product import ProductBrokerAdapter
from src.infrastructure.broker.consumers.schemas.order import OrderBrokerSchema

rmq_product_router = RabbitRouter(prefix="product-")


@rmq_product_router.subscriber("purchase", exchange="product")
@inject
async def purchase_product(
        order_schema: OrderBrokerSchema,
        product_broker_adapter: FromDishka[ProductBrokerAdapter],
) -> None:
    await product_broker_adapter.purchase_product(order_schema)
