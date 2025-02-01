from dataclasses import dataclass, field

from src.domain.values.category import Category


@dataclass
class ProductDTO:
    name: str
    category: Category
    quantity: int
    price: int


@dataclass
class UpdateProductDTO(ProductDTO):
    name: str | None = field(default=None, kw_only=True)
    category: Category | None = field(default=None, kw_only=True)
    quantity: int | None = field(default=None, kw_only=True)
    price: int | None = field(default=None, kw_only=True)
