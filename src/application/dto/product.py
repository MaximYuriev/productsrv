from dataclasses import dataclass

from src.domain.values.category import Category


@dataclass
class ProductDTO:
    name: str
    category: Category
    quantity: int
    price: int
