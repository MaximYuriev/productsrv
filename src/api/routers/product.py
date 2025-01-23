from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter

from src.api.adapters.product import FromRouterToProductServiceAdapter
from src.api.responses.product import ProductResponse
from src.api.schemas.product import CreateProductSchema

product_router = APIRouter(prefix="/product", tags=["Product"])


@product_router.post("")
@inject
async def create_new_product(
        created_product_schema: CreateProductSchema,
        product_adapter: FromDishka[FromRouterToProductServiceAdapter],
):
    await product_adapter.create_new_product(created_product_schema)
    return ProductResponse(detail="Товар успешно добавлен!")
