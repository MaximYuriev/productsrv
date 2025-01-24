from src.application.exceptions.base import ProductServiceException


class BaseProductException(ProductServiceException):
    pass


class ProductNotFoundException(BaseProductException):
    @property
    def message(self) -> str:
        return "Товар не найден!"


class ProductNameNotUniqueException(BaseProductException):
    @property
    def message(self) -> str:
        return "Название товара должно быть уникально!"
