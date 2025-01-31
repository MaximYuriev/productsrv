import jwt

from config import PRIVATE_KEY_PATH, PUBLIC_KEY_PATH
from .payloads import BasePayload
from .exceptions import AuthTokenInvalidException, AuthTokenExpiredException


class JWT:
    __CRYPT_ALGORITHM = 'RS256'
    __PUBLIC_KEY = PUBLIC_KEY_PATH.read_text()
    __PRIVATE_KEY = PRIVATE_KEY_PATH.read_text()

    @classmethod
    def create_jwt(
            cls,
            payload: BasePayload,
    ):
        token_data = payload.__dict__
        return jwt.encode(
            token_data,
            cls.__PRIVATE_KEY,
            algorithm=cls.__CRYPT_ALGORITHM
        )

    @classmethod
    def parse_jwt(
            cls,
            token: str,
            verify_expire: bool = True
    ):
        try:
            return jwt.decode(
                token,
                cls.__PUBLIC_KEY,
                algorithms=[cls.__CRYPT_ALGORITHM],
                options={
                    "verify_exp": verify_expire,
                }
            )
        except jwt.ExpiredSignatureError:
            raise AuthTokenExpiredException
        except jwt.InvalidTokenError:
            raise AuthTokenInvalidException
