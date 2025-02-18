from pydantic import BaseModel, Field


class PurchaseProductBrokerSchema(BaseModel):
    product_id: int
    quantity_on_basket: int = Field(serialization_alias="quantity")
