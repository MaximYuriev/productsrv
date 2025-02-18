import uuid

from pydantic import BaseModel, Field

from src.infrastructure.broker.consumers.schemas.product import PurchaseProductBrokerSchema


class OrderBrokerSchema(BaseModel):
    order_id: uuid.UUID
    basket_id: uuid.UUID
    products: list[PurchaseProductBrokerSchema] = Field(exclude=True)
