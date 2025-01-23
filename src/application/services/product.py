from src.application.dto.product import ProductDTO
from src.application.interfaces.repositories.product import IProductRepository
from src.domain.models.product import Product


class ProductService:
    def __init__(self, repository: IProductRepository) -> None:
        self._repository = repository

    async def create_new_product(self, created_product: ProductDTO) -> None:
        product = Product(**created_product.__dict__)
        await self._repository.add(product)
