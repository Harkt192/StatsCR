from fastapi import HTTPException, APIRouter, Form
from fastapi.responses import JSONResponse

from core.db import SessionDep
from users.schemes import UserGetScheme, UserCreateScheme, UserScheme, TokenInfo
from users.service import UserService
from users.auth import PayloadDep, UserDep, validate_user

from users.utils import (
    encode_jwt,
    decode_jwt,
    hash_password,
    validate_password
)


users_rt = APIRouter(prefix="/users", tags=["User management"])


@users_rt.get("", response_class=JSONResponse)
async def get_users(session: SessionDep):
    users = await UserService.get_all(session=session)
    return users


@users_rt.post("/create", response_class=JSONResponse)
async def create_user(user_data: UserCreateScheme, session: SessionDep):
    user = await UserService.create(user_data=user_data, session=session)
    return user


@users_rt.get("/{user_id}", response_class=JSONResponse)
async def get_user_by_id(user_id: int, session: SessionDep) -> UserGetScheme:
    user = await UserService.get(user_id=user_id, session=session)
    if not user:
        return HTTPException(404, "Пользователь не найден")
    return user


@users_rt.patch("/change", response_class=JSONResponse)
async def update_user(user_data: UserGetScheme, session: SessionDep):
    user = await UserService.update(user_data=user_data, session=session)
    return user


@users_rt.post("/login", response_model=TokenInfo)
async def login_user(
        session: SessionDep,
        email: str = Form(),
        password: str = Form()
):
    user = await validate_user(session=session, email=email, password=password)
    jwt_payload = {
        "id": user.id,
        "sub": user.email,
    }
    token = await encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@users_rt.get("/users/me")
async def profile(
    payload: dict = PayloadDep,
    user: UserScheme = UserDep,
):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }
