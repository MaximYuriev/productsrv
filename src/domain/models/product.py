from dataclasses import dataclass, field


@dataclass
class Product:
    product_id: int | None = field(default=None, kw_only=True)
    name: str
    quantity: int
    price: int
