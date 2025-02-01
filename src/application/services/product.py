from src.application.dto.product import ProductDTO, UpdateProductDTO
from src.application.exceptions.product import ProductNameNotUniqueException, ProductNotFoundException
from src.application.interfaces.broker.product import IProductPublisher
from src.application.interfaces.repositories.product import IProductRepository
from src.domain.models.product import Product


class ProductService:
    def __init__(self, repository: IProductRepository, publisher: IProductPublisher) -> None:
        self._repository = repository
        self._publisher = publisher

    async def create_new_product(self, created_product: ProductDTO) -> None:
        await self._validate_product_name(created_product.name)
        product = Product(**created_product.__dict__)
        product.product_id = await self._repository.add(product)
        await self._publisher.publish_create_product(product)

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

    async def delete_product(self, product_id: int) -> None:
        product = await self.get_one_product(product_id)
        await self._repository.delete_product(product)
        await self._publisher.publish_delete_product(product)

    async def update_product(self, product_id: int, update_product: UpdateProductDTO) -> None:
        if update_product.name:
            await self._validate_product_name(update_product.name)
        product = await self._repository.update_product(product_id, update_product)
        if update_product.name or update_product.price:
            await self._publisher.publish_update_product(product)

    async def _validate_product_name(self, product_name: str) -> None:
        try:
            await self._repository.get_product_by_name(product_name)
        except ProductNotFoundException:
            pass
        else:
            raise ProductNameNotUniqueException
