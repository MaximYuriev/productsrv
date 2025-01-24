from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.models.base import Base


class ProductModel(Base):
    __tablename__ = "product"
    product_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    category: Mapped[str]
    quantity: Mapped[int]
    price: Mapped[int]
