import uuid

from aio_pika import RobustExchange, RobustQueue
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue

from src.application.dto.order import OrderDTO
from src.application.interfaces.broker.product import IProductPublisher
from src.domain.models.product import Product
from src.infrastructure.broker.publishers.schemas.base import PublishBrokerSchema
from src.infrastructure.broker.publishers.schemas.basket import ClearBasketSchema
from src.infrastructure.broker.publishers.schemas.order import CancelOrderSchema, AcceptOrderSchema
from src.infrastructure.broker.publishers.schemas.product import CreateProductBrokerSchema, \
    DeleteProductBrokerSchema, UpdateProductBrokerSchema


class RMQProductPublisher(IProductPublisher):
    _PRODUCT_EXCHANGE_NAME = "product"
    _ORDER_EXCHANGE_NAME = "order"
    _BASKET_EXCHANGE_NAME = "basket"
    _CREATE_PRODUCT_QUEUE_NAME = "product-create"
    _UPDATE_PRODUCT_QUEUE_NAME = "product-update"
    _DELETE_PRODUCT_QUEUE_NAME = "product-delete"
    _CANCEL_ORDER_QUEUE_NAME = "order-cancel"
    _ACCEPT_ORDER_QUEUE_NAME = "order-accept"
    _CLEAR_BASKET_QUEUE_NAME = "basket-clear"

    def __init__(self, broker: RabbitBroker):
        self._broker = broker

    async def publish_delete_product(self, product: Product) -> None:
        exchange, queue = await self._prepare_to_publish(
            exchange_name=self._PRODUCT_EXCHANGE_NAME,
            queue_name=self._DELETE_PRODUCT_QUEUE_NAME,
        )
        product_schema = DeleteProductBrokerSchema.model_validate(product, from_attributes=True)
        await self._publish(exchange, queue, product_schema)

    async def publish_create_product(self, product: Product) -> None:
        exchange, queue = await self._prepare_to_publish(
            exchange_name=self._PRODUCT_EXCHANGE_NAME,
            queue_name=self._CREATE_PRODUCT_QUEUE_NAME,
        )
        product_schema = CreateProductBrokerSchema.model_validate(product, from_attributes=True)
        await self._publish(exchange, queue, product_schema)

    async def publish_update_product(self, product: Product) -> None:
        exchange, queue = await self._prepare_to_publish(
            exchange_name=self._PRODUCT_EXCHANGE_NAME,
            queue_name=self._UPDATE_PRODUCT_QUEUE_NAME,
        )
        product_schema = UpdateProductBrokerSchema.model_validate(product, from_attributes=True)
        await self._publish(exchange, queue, product_schema)

    async def cancel_order(self, order_id: uuid.UUID, reason: str) -> None:
        exchange, queue = await self._prepare_to_publish(
            exchange_name=self._ORDER_EXCHANGE_NAME,
            queue_name=self._CANCEL_ORDER_QUEUE_NAME,
        )
        order_schema = CancelOrderSchema(order_id=order_id, reason=reason)
        await self._publish(exchange, queue, order_schema)

    async def accept_order(self, order: OrderDTO) -> None:
        exchange, queue = await self._prepare_to_publish(
            exchange_name=self._ORDER_EXCHANGE_NAME,
            queue_name=self._ACCEPT_ORDER_QUEUE_NAME,
        )
        order_schema = AcceptOrderSchema.model_validate(order, from_attributes=True)
        await self._publish(exchange, queue, order_schema)

    async def clear_basket(self, order: OrderDTO) -> None:
        exchange, queue = await self._prepare_to_publish(
            exchange_name=self._BASKET_EXCHANGE_NAME,
            queue_name=self._CLEAR_BASKET_QUEUE_NAME,
        )
        basket_schema = ClearBasketSchema.model_validate(order, from_attributes=True)
        await self._publish(exchange, queue, basket_schema)

    async def _prepare_to_publish(self, exchange_name: str, queue_name: str) -> tuple[RobustExchange, RobustQueue]:
        exchange = await self._declare_exchange(exchange_name)
        queue = await self._declare_queue(queue_name)
        await self._bind_queue_to_exchange(exchange, queue)
        return exchange, queue

    async def _publish(
            self,
            exchange: RobustExchange,
            queue: RobustQueue,
            published_schema: PublishBrokerSchema,
    ) -> None:
        await self._broker.publish(
            message=published_schema,
            exchange=exchange.name,
            routing_key=queue.name,
        )

    async def _declare_exchange(self, exchange_name: str) -> RobustExchange:
        exchange = RabbitExchange(exchange_name)
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
