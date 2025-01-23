from pydantic import BaseModel


class BaseResponse(BaseModel):
    detail: str
    data: str | None = None
