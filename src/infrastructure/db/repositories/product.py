from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repositories.product import IProductRepository
from src.domain.models.product import Product
from src.infrastructure.db.models.product import ProductModel


class ProductRepository(IProductRepository):
    domain = Product
    model = ProductModel

    def __init__(self, session: AsyncSession):
        self._session = session

    def _convert_domain_to_model(self, product: Product) -> ProductModel:
        return self.model(
            product_id=product.product_id,
            name=product.name,
            quantity=product.quantity,
            price=product.price,
        )

    async def add(self, product: Product) -> None:
        product_model = self._convert_domain_to_model(product)
        self._session.add(product_model)
        await self._session.commit()
