from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, HTTPException, status

from src.api.adapters.product import FromRouterToProductServiceAdapter
from src.api.responses.product import ProductResponse
from src.api.schemas.product import CreateProductSchema
from src.application.exceptions.product import ProductNameNotUniqueException, ProductNotFoundException

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


@product_router.get("/{product_id}")
@inject
async def get_product_by_id(
        product_id: int,
        product_adapter: FromDishka[FromRouterToProductServiceAdapter],
):
    try:
        product = await product_adapter.get_product_by_id(product_id)
    except ProductNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message,
        )
    else:
        return ProductResponse(detail="Товар найден!", data=product)
