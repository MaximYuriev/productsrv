from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, Field


class ProductSchema(BaseModel):
    name: str
    quantity: int
    price: int


class CreateProductSchema(ProductSchema):
    name: Annotated[str, MinLen(5), MaxLen(20)]
    quantity: int = Field(gt=0, le=1000)
    price: int = Field(ge=0)
