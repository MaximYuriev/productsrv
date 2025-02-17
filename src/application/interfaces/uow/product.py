from abc import ABC, abstractmethod

from src.application.interfaces.repositories.product import IProductRepository
from src.application.interfaces.uow.base import BaseUoW


class IProductUoW(BaseUoW, ABC):
    @property
    @abstractmethod
    def product_repository(self) -> IProductRepository:
        pass
