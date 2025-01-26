from src.application.dto.product import ProductDTO
from src.application.exceptions.product import ProductNameNotUniqueException, ProductNotFoundException
from src.application.interfaces.repositories.product import IProductRepository
from src.domain.models.product import Product
from src.domain.values.category import Category


class ProductService:
    def __init__(self, repository: IProductRepository) -> None:
        self._repository = repository

    async def create_new_product(self, created_product: ProductDTO) -> None:
        product = Product(**created_product.__dict__)
        await self._validate_product_name(product.name)
        await self._repository.add(product)

    async def get_one_product(self, product_id: int) -> Product:
        return await self._repository.get_product_by_id(product_id)

    async def get_list_products(
            self,
            page_number: int,
            page_size: int,
            **kwargs,
    ) -> list[Product]:
        offset = page_number - 1
        return await self._repository.get_products(offset=offset, limit=page_size, **kwargs)

    async def _validate_product_name(self, product_name: str) -> None:
        try:
            await self._repository.get_product_by_name(product_name)
        except ProductNotFoundException:
            pass
        else:
            raise ProductNameNotUniqueException
