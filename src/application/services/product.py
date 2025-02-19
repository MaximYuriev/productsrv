from src.application.dto.order import OrderDTO
from src.application.dto.product import ProductDTO, UpdateProductDTO
from src.application.exceptions.product import ProductNameNotUniqueException, ProductNotFoundException
from src.application.interfaces.broker.product import IProductPublisher
from src.application.interfaces.uow.product import IProductUoW
from src.domain.models.product import Product


class ProductService:
    def __init__(self, uow: IProductUoW, publisher: IProductPublisher) -> None:
        self._uow = uow
        self._publisher = publisher

    async def create_new_product(self, created_product: ProductDTO) -> None:
        async with self._uow:
            await self._validate_product_name(created_product.name)
            product = Product(**created_product.__dict__)
            product.product_id = await self._uow.product_repository.add(product)
            await self._publisher.publish_create_product(product)
            await self._uow.commit()

    async def get_one_product(self, product_id: int) -> Product:
        async with self._uow:
            return await self._uow.product_repository.get_product_by_id(product_id)

    async def get_list_products(
            self,
            page_number: int,
            page_size: int,
            **kwargs,
    ) -> list[Product]:
        async with self._uow:
            offset = page_number - 1
            return await self._uow.product_repository.get_products(offset=offset, limit=page_size, **kwargs)

    async def delete_product(self, product_id: int) -> None:
        async with self._uow:
            product = await self.get_one_product(product_id)
            await self._uow.product_repository.delete_product(product)
            await self._publisher.publish_delete_product(product)
            await self._uow.commit()

    async def update_product(self, product_id: int, update_product: UpdateProductDTO) -> None:
        async with self._uow:
            if update_product.name is not None:
                await self._validate_product_name(update_product.name)
            product = await self._uow.product_repository.update_product(product_id, update_product)
            if update_product.name is not None or update_product.price is not None:
                await self._publisher.publish_update_product(product)
            await self._uow.commit()

    async def purchase_product(self, order: OrderDTO) -> None:
        async with self._uow:
            for purchased_product in order.purchased_product_list:
                try:
                    product = await self._uow.product_repository.get_product_by_id(purchased_product.product_id)
                except ProductNotFoundException:
                    await self._publisher.cancel_order(
                        order.order_id,
                        reason=f"Товар с id = {purchased_product.product_id} не найден!",
                    )
                else:
                    if product.quantity >= purchased_product.quantity:
                        update_product = UpdateProductDTO(
                            quantity=product.quantity - purchased_product.quantity,
                        )
                        await self._uow.product_repository.update_product(product.product_id, update_product)
                    else:
                        await self._publisher.cancel_order(
                            order.order_id,
                            reason=f"На складе нет указанного количества товара. Товар с id = {product.product_id}"
                                   f"имеется в количестве {product.quantity}."
                                   f"Было запрошено - {purchased_product.quantity}"
                        )
                        await self._uow.rollback()
                        return
            await self._uow.commit()

    async def _validate_product_name(self, product_name: str) -> None:
        try:
            await self._uow.product_repository.get_product_by_name(product_name)
        except ProductNotFoundException:
            pass
        else:
            raise ProductNameNotUniqueException
