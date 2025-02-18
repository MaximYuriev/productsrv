from src.infrastructure.broker.publishers.schemas.base import PublishBrokerSchema


class CreateProductBrokerSchema(PublishBrokerSchema):
    product_id: int
    name: str
    price: int


class UpdateProductBrokerSchema(PublishBrokerSchema):
    product_id: int
    name: str | None = None
    price: int | None = None


class DeleteProductBrokerSchema(PublishBrokerSchema):
    product_id: int
