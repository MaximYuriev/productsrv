from fastapi import HTTPException, status


class HTTPBaseProductException(HTTPException):
    pass


class HTTPProductNameNotUniqueException(HTTPBaseProductException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )


class HTTPProductNotFoundException(HTTPBaseProductException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg,
        )
