import uuid

from pydantic import Field

from src.infrastructure.broker.publishers.schemas.base import PublishBrokerSchema
from src.infrastructure.broker.publishers.schemas.product import PurchasedProductPublishSchema


class ClearBasketSchema(PublishBrokerSchema):
    basket_id: uuid.UUID
    products_on_basket: list[PurchasedProductPublishSchema] = Field(validation_alias="purchased_product_list")
