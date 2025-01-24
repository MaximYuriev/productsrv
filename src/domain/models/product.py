from dataclasses import dataclass, field

from src.domain.values.category import Category


@dataclass
class Product:
    product_id: int | None = field(default=None, kw_only=True)
    name: str
    category: Category
    quantity: int
    price: int
