from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)
from flask import session
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


auth_rt = APIRouter(prefix="/jwt", tags=["JWT"])


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/jwt/login",
)


class TokenInfo(BaseModel):
    access_token: str
    token_type: str



async def validate_auth_user(
        session_dep: AsyncSession,
        email: str,
        password: str,
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
    )
    query = select(User).where(email == User.email)
    result = await session_dep.execute(query)
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


async def get_current_token_payload(
        token: str = Depends(oauth2_scheme),
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
        session_dep: SessionDep,
        payload: dict = Depends(get_current_token_payload),
) -> UserLoginScheme:
    email: str = payload.get("sub")
    query = select(User).where(email == User.email)
    result = await session_dep.execute(query)
    user = result.scalars().first()
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


async def get_current_active_auth_user(
    user: UserScheme = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


@auth_rt.post("/login", response_model=TokenInfo)
async def auth_user_issue_jwt(
        session_: SessionDep,
        email: str = Form(),
        password: str = Form()
):
    user = await validate_auth_user(session_dep=session_, email=email, password=password)
    jwt_payload = {
        "id": user.id,
        "sub": user.email,
    }
    token = await encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@auth_rt.get("/users/me")
async def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserScheme = Depends(get_current_active_auth_user),
):
    print(payload)
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }