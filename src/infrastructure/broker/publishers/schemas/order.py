import uuid

from src.infrastructure.broker.publishers.schemas.base import PublishBrokerSchema


class CancelOrderSchema(PublishBrokerSchema):
    order_id: uuid.UUID
    reason: str
