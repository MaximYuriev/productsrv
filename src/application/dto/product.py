from dataclasses import dataclass


@dataclass
class ProductDTO:
    name: str
    quantity: int
    price: int
