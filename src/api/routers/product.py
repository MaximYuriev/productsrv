from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, HTTPException, status

from src.api.adapters.product import FromRouterToProductServiceAdapter
from src.api.responses.product import ProductResponse
from src.api.schemas.product import CreateProductSchema
from src.application.exceptions.product import ProductNameNotUniqueException

product_router = APIRouter(prefix="/product", tags=["Product"])


@product_router.post("")
@inject
async def create_new_product(
        created_product_schema: CreateProductSchema,
        product_adapter: FromDishka[FromRouterToProductServiceAdapter],
):
    try:
        await product_adapter.create_new_product(created_product_schema)
    except ProductNameNotUniqueException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.message,
        )
    else:
        return ProductResponse(detail="Товар успешно добавлен!")
