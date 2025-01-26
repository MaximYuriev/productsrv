from pydantic import BaseModel, Field, field_serializer

from src.domain.values.category import Category


class PaginationQueryParams(BaseModel):
    pn: int = Field(default=1, ge=1, description="Page number", serialization_alias="page_number")
    ps: int = Field(default=5, ge=1, description="Page size", serialization_alias="page_size")


class PaginationQueryParamsWithCategory(PaginationQueryParams):
    category: Category | None = None

    @field_serializer('category')
    def serialize_dt(self, category: Category):
        return category.value
