from typing import Annotated

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, HTTPException, status, Query

from src.api.adapters.product import FromRouterToProductServiceAdapter
from src.api.exceptions.product import HTTPProductNameNotUniqueException, HTTPProductNotFoundException
from src.api.responses.product import ProductResponse
from src.api.schemas.pagination import PaginationQueryParamsWithCategory
from src.api.schemas.product import CreateProductSchema, UpdateProductSchema
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
        raise HTTPProductNameNotUniqueException(exc.message)
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
        raise HTTPProductNotFoundException(exc.message)
    else:
        return ProductResponse(detail="Товар найден!", data=product)


@product_router.get("")
@inject
async def get_products(
        pagination_params: Annotated[PaginationQueryParamsWithCategory, Query()],
        product_adapter: FromDishka[FromRouterToProductServiceAdapter],
):
    products = await product_adapter.get_list_products(pagination_params)
    return ProductResponse(detail="Найденные товары", data=products)


@product_router.delete("/{product_id}")
@inject
async def delete_product(
        product_id: int,
        product_adapter: FromDishka[FromRouterToProductServiceAdapter],
):
    try:
        await product_adapter.delete_product(product_id)
    except ProductNotFoundException as exc:
        raise HTTPProductNotFoundException(exc.message)
    else:
        return ProductResponse(detail="Товар успешно удален!")


@product_router.patch("/{product_id}")
@inject
async def update_product(
        product_id: int,
        update_product_schema: UpdateProductSchema,
        product_adapter: FromDishka[FromRouterToProductServiceAdapter],
):
    try:
        await product_adapter.update_product(product_id, update_product_schema)
    except ProductNotFoundException as exc:
        raise HTTPProductNotFoundException(exc.message)
    except ProductNameNotUniqueException as exc:
        raise HTTPProductNameNotUniqueException(exc.message)
    else:
        return ProductResponse(detail="Товар успешно изменен!")
