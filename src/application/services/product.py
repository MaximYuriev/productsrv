from src.application.dto.product import ProductDTO
from src.application.exceptions.product import ProductNameNotUniqueException, ProductNotFoundException
from src.application.interfaces.repositories.product import IProductRepository
from src.domain.models.product import Product


class ProductService:
    def __init__(self, repository: IProductRepository) -> None:
        self._repository = repository

    async def create_new_product(self, created_product: ProductDTO) -> None:
        product = Product(**created_product.__dict__)
        await self._validate_product_name(product.name)
        await self._repository.add(product)

    async def _validate_product_name(self, product_name: str) -> None:
        try:
            await self._repository.get_product_by_name(product_name)
        except ProductNotFoundException:
            pass
        else:
            raise ProductNameNotUniqueException
