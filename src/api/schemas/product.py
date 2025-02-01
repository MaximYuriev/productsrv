from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, Field, field_serializer

from src.domain.values.category import Category


class ProductSchema(BaseModel):
    name: str
    category: Category
    quantity: int
    price: int


class CreateProductSchema(ProductSchema):
    name: Annotated[str, MinLen(5), MaxLen(20)]
    quantity: int = Field(gt=0, le=1000)
    price: int = Field(gt=0)


class UpdateProductSchema(ProductSchema):
    name: str | None = Field(default=None, min_length=5, max_length=20)
    category: Category | None = None
    quantity: int | None = Field(default=None, gt=0, le=1000)
    price: int | None = Field(default=None, gt=0)

    @field_serializer('category')
    def serialize_category(self, category: Category | None):
        return category.value if category is not None else None

class ProductSchemaForResponse(ProductSchema):
    product_id: int
