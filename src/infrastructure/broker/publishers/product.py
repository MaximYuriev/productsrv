from aio_pika import RobustExchange, RobustQueue
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue

from src.application.interfaces.broker.product import IProductPublisher
from src.domain.models.product import Product
from src.infrastructure.broker.schemas.product import CreateProductBrokerSchema, ProductBrokerSchema, \
    DeleteProductBrokerSchema, UpdateProductBrokerSchema


class RMQProductPublisher(IProductPublisher):
    _EXCHANGE_NAME = "product"
    _CREATE_PRODUCT_QUEUE_NAME = "product-create"
    _UPDATE_PRODUCT_QUEUE_NAME = "product-update"
    _DELETE_PRODUCT_QUEUE_NAME = "product-delete"

    def __init__(self, broker: RabbitBroker):
        self._broker = broker

    async def publish_create_product(self, product: Product) -> None:
        exchange, queue = await self._prepare_to_publish(self._CREATE_PRODUCT_QUEUE_NAME)
        product_schema = CreateProductBrokerSchema.model_validate(product, from_attributes=True)
        await self._publish(exchange, queue, product_schema)

    async def publish_delete_product(self, product: Product) -> None:
        exchange, queue = await self._prepare_to_publish(self._DELETE_PRODUCT_QUEUE_NAME)
        product_schema = DeleteProductBrokerSchema.model_validate(product, from_attributes=True)
        await self._publish(exchange, queue, product_schema)

    async def publish_update_product(self, product: Product) -> None:
        exchange, queue = await self._prepare_to_publish(self._UPDATE_PRODUCT_QUEUE_NAME)
        product_schema = UpdateProductBrokerSchema.model_validate(product, from_attributes=True)
        await self._publish(exchange, queue, product_schema)

    async def _prepare_to_publish(self, queue_name: str) -> tuple[RobustExchange, RobustQueue]:
        exchange = await self._declare_exchange()
        queue = await self._declare_queue(queue_name)
        await self._bind_queue_to_exchange(exchange, queue)
        return exchange, queue

    async def _publish(
            self,
            exchange: RobustExchange,
            queue: RobustQueue,
            product_schema: ProductBrokerSchema,
    ) -> None:
        await self._broker.publish(
            message=product_schema,
            exchange=exchange.name,
            routing_key=queue.name,
        )

    async def _declare_exchange(self) -> RobustExchange:
        exchange = RabbitExchange(self._EXCHANGE_NAME)
        return await self._broker.declare_exchange(exchange)

    async def _declare_queue(self, queue_name: str) -> RobustQueue:
        rabbit_queue = RabbitQueue(queue_name)
        queue = await self._broker.declare_queue(rabbit_queue)
        return queue

    @staticmethod
    async def _bind_queue_to_exchange(exchange: RobustExchange, queue: RobustQueue) -> None:
        await queue.bind(
            exchange=exchange.name,
            routing_key=queue.name,
        )
