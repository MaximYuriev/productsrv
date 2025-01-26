from src.api.responses.base import BaseResponse
from src.api.schemas.product import ProductSchemaForResponse


class ProductResponse(BaseResponse):
    data: ProductSchemaForResponse | list[ProductSchemaForResponse] | None = None
