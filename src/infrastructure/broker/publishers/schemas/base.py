from abc import ABC

from pydantic import BaseModel


class PublishBrokerSchema(BaseModel, ABC):
    pass
