from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.exceptions.product import ProductNotFoundException
from src.application.interfaces.repositories.product import IProductRepository
from src.domain.models.product import Product
from src.domain.values.category import Category
from src.infrastructure.db.models.product import ProductModel


class ProductRepository(IProductRepository):
    domain = Product
    model = ProductModel

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, product: Product) -> None:
        product_model = self._convert_domain_to_model(product)
        self._session.add(product_model)
        await self._session.commit()

    async def get_product_by_name(self, product_name: str) -> Product:
        product_model = await self._get_product_model(name=product_name)
        return self._convert_model_to_domain(product_model)

    async def get_product_by_id(self, product_id: int) -> Product:
        product_model = await self._get_product_model(product_id=product_id)
        return self._convert_model_to_domain(product_model)

    def _convert_domain_to_model(self, product: Product) -> ProductModel:
        return self.model(
            product_id=product.product_id,
            name=product.name,
            category=product.category.value,
            quantity=product.quantity,
            price=product.price,
        )

    def _convert_model_to_domain(self, product_model: ProductModel) -> Product:
        return self.domain(
            product_id=product_model.product_id,
            name=product_model.name,
            category=Category(product_model.category),
            quantity=product_model.quantity,
            price=product_model.price,
        )

    async def _get_product_model(self, **kwargs) -> ProductModel:
        product_model = await self._session.scalar(select(ProductModel).filter_by(**kwargs))
        if product_model is not None:
            return product_model
        raise ProductNotFoundException
