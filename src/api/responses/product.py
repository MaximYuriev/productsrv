from src.api.responses.base import BaseResponse
from src.api.schemas.product import ProductSchema


class ProductResponse(BaseResponse):
    data: ProductSchema | None = None
