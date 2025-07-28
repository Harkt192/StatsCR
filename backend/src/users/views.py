from fastapi import HTTPException, APIRouter, Form
from fastapi.responses import JSONResponse

from core.db import SessionDep
from users.schemes import UserGetScheme, UserCreateScheme, UserScheme, TokenInfo
from users.service import UserService
from users.auth import PayloadDep, UserDep, validate_user
from users.models import User
from users.utils import (
    encode_jwt,
    decode_jwt,
    hash_password,
    validate_password
)
from request_utils import ApiManager
from log import logger


users_rt = APIRouter(prefix="/users", tags=["User management"])


@users_rt.get("", response_class=JSONResponse)
async def get_users(
        session: SessionDep
):
    users = await UserService.get_all(session=session)
    return users


@users_rt.post("/create", response_class=JSONResponse)
async def create_user(
        session: SessionDep,
        user_data: UserCreateScheme
):
    await UserService.create(user_data=user_data, session=session)
    return {"status": 200}


@users_rt.patch("/change", response_class=JSONResponse)
async def update_user(
        session: SessionDep,
        user_data: UserGetScheme,
):
    await UserService.update(user_data=user_data, session=session)
    return {"status": 200}


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
        "game_id": user.game_id
    }
    token = await encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@users_rt.get("/me")
async def me(
        payload: dict = PayloadDep,
        user: UserScheme = UserDep
):
    logger.info(f"Payload: {payload}")
    player_data = await ApiManager.getPlayerInfo(user.game_id)
    return player_data


@users_rt.get("/profile")
async def profile(
        payload: dict = PayloadDep,
        user: UserScheme = UserDep,
):
    logger.info(f"Payload: {payload}")
    return {
        "id": user.id,
        "email": user.email,
        "game_id": user.game_id
    }


@users_rt.get("/{user_id}", response_class=JSONResponse)
async def get_user_by_id(
        session: SessionDep,
        user_id: int
) -> UserScheme:
    user = await UserService.get(user_id=user_id, session=session)
    if not user:
        return HTTPException(404, "Пользователь не найден")
    return user
