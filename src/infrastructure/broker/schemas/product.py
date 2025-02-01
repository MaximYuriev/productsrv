from abc import ABC

from pydantic import BaseModel


class ProductBrokerSchema(BaseModel, ABC):
    pass


class CreateProductBrokerSchema(ProductBrokerSchema):
    product_id: int
    name: str
    price: int


class UpdateProductBrokerSchema(ProductBrokerSchema):
    product_id: int
    name: str | None = None
    price: int | None = None


class DeleteProductBrokerSchema(ProductBrokerSchema):
    product_id: int
