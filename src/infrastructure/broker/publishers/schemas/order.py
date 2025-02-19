import uuid

from pydantic import Field

from src.infrastructure.broker.publishers.schemas.base import PublishBrokerSchema
from src.infrastructure.broker.publishers.schemas.product import PurchasedProductPublishSchema


class CancelOrderSchema(PublishBrokerSchema):
    order_id: uuid.UUID
    reason: str


class AcceptOrderSchema(PublishBrokerSchema):
    order_id: uuid.UUID
    products_on_order: list[PurchasedProductPublishSchema] = Field(validation_alias="purchased_product_list")
