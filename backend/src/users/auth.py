from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
    Request
)
from pydantic import BaseModel
from core.db import SessionDep
from users.schemes import UserLoginScheme, UserScheme
from users.utils import (
    encode_jwt,
    decode_jwt,
    hash_password,
    validate_password
)
from users.models import User
from settings import settings

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from jwt import InvalidTokenError


async def validate_user(
        session: AsyncSession,
        email: str,
        password: str,
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
    )
    query = select(User).where(email == User.email)
    result = await session.execute(query)
    user = result.scalars().first()
    if not user:
        raise unauthed_exc
    if not await validate_password(
        password=password,
        hashed_password=user.password,
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


async def get_token_from_headers(
        request: Request
):
    authorization = request.headers.get("Authorization")
    token_type, token = authorization.split()
    if token_type.lower() != "bearer":
        raise HTTPException(
            status_code=452,
            detail="Bad authorization token type"
        )
    return token


async def get_token_payload(
        token: str = Depends(get_token_from_headers),
) -> dict:
    try:
        payload = await decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


async def get_current_auth_user(
        session: SessionDep,
        payload: dict = Depends(get_token_payload),
) -> User:
    email: str = payload.get("sub")
    query = select(User).where(email == User.email)
    result = await session.execute(query)
    user = result.scalars().first()
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


async def get_current_active_auth_user(
    user: UserScheme = Depends(get_current_auth_user),
) -> User:
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


PayloadDep: dict = Depends(get_token_payload)
UserDep: UserScheme = Depends(get_current_active_auth_user)
