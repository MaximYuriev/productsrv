from src.api.schemas.pagination import PaginationQueryParams
from src.api.schemas.product import CreateProductSchema, ProductSchemaForResponse
from src.application.dto.product import ProductDTO
from src.application.services.product import ProductService
from src.domain.models.product import Product


class FromRouterToProductServiceAdapter:
    def __init__(self, service: ProductService):
        self._service = service

    async def create_new_product(self, created_product_schema: CreateProductSchema) -> None:
        create_product_data = created_product_schema.model_dump()
        product = ProductDTO(**create_product_data)
        await self._service.create_new_product(product)

    async def get_product_by_id(self, product_id: int) -> ProductSchemaForResponse:
        product = await self._service.get_one_product(product_id)
        return self._convert_domain_to_response(product)

    async def get_list_products(self, pagination_params: PaginationQueryParams) -> list[ProductSchemaForResponse]:
        pagination_params = pagination_params.model_dump(by_alias=True, exclude_none=True)
        products = await self._service.get_list_products(**pagination_params)
        return [self._convert_domain_to_response(product) for product in products]

    @staticmethod
    def _convert_domain_to_response(product: Product) -> ProductSchemaForResponse:
        return ProductSchemaForResponse(
            product_id=product.product_id,
            name=product.name,
            category=product.category,
            quantity=product.quantity,
            price=product.price,
        )
