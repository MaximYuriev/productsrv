import uuid
from typing import Annotated

from fastapi import Depends, Request

from authorizer.auth.exceptions import AuthTokenInvalidException
from authorizer.authorizer import Authorizer
from authorizer.http.exceptions import HTTPUnauthorizedException, HTTPTokenInvalidException
from config import COOKIE_KEY_NAME


def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get(COOKIE_KEY_NAME)
    if token is not None:
        return token
    raise HTTPUnauthorizedException


def get_user_id_from_token(token: Annotated[str, Depends(get_token_from_cookie)]) -> uuid.UUID:
    try:
        return Authorizer.get_user_id_from_token(token)
    except AuthTokenInvalidException:
        raise HTTPTokenInvalidException
