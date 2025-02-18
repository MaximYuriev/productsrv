import uuid
from dataclasses import dataclass

from src.application.dto.product import PurchasedProductDTO


@dataclass()
class OrderDTO:
    order_id: uuid.UUID
    basket_id: uuid.UUID
    purchased_product_list: list[PurchasedProductDTO]
