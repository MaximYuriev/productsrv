from dataclasses import dataclass, field

from src.domain.values.id.product import ProductId


@dataclass
class Product:
    product_id: int = field(default_factory=lambda: ProductId().id, kw_only=True)
    name: str
    quantity: int
    price: int
