from src.api.schemas.product import CreateProductSchema
from src.application.dto.product import ProductDTO
from src.application.services.product import ProductService


class FromRouterToProductServiceAdapter:
    def __init__(self, service: ProductService):
        self._service = service

    async def create_new_product(self, created_product_schema: CreateProductSchema) -> None:
        create_product_data = created_product_schema.model_dump()
        product = ProductDTO(**create_product_data)
        await self._service.create_new_product(product)
