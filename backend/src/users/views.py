from fastapi import HTTPException, APIRouter, Form
from fastapi.responses import JSONResponse

from core.db import SessionDep
from users.schemes import UserGetScheme, UserCreateScheme, UserScheme, TokenInfo
from users.service import UserService
from users.auth import PayloadDep, UserDep, validate_user
from users.models import User
from users.utils import encode_jwt
from cr_utils import (
    ApiManager,
    reformat_player_data,
    reformat_battlelog_data
)
from log import logger

from app import redis_service


users_rt = APIRouter(prefix="/users", tags=["User management"])


@users_rt.get(
    "",
    response_class=JSONResponse
)
async def get_users(
        session: SessionDep
):
    users = await UserService.get_all(session=session)
    return users


@users_rt.get(
    "/{user_id:int}",
    response_class=JSONResponse
)
async def get_user_by_id(
        session: SessionDep,
        user_id: int
) -> UserScheme:
    user = await UserService.get(user_id=user_id, session=session)
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    return user


@users_rt.post(
    "/create",
    response_class=JSONResponse
)
async def create_user(
        session: SessionDep,
        user_data: UserCreateScheme
):
    await UserService.create(user_data=user_data, session=session)
    return {"status": 200}


@users_rt.patch(
    "/change",
    response_class=JSONResponse
)
async def update_user(
        session: SessionDep,
        user_data: UserScheme,
):
    await UserService.update(user_data=user_data, session=session)
    return {"status": 200}


@users_rt.post(
    "/login",
    response_model=TokenInfo
)
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
    token = encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@users_rt.get(
    "/me",
    response_class=JSONResponse
)
async def me(
        payload: dict = PayloadDep,
        user: UserScheme = UserDep
):
    logger.info(f"Payload: {payload}")
    key = f"{user.email}-me"
    ttl = 20
    cash_data = await redis_service.get(key)
    logger.info(f"Ключ Redis: {key}")
    logger.info(f"Данные кэша: {cash_data}")
    if not cash_data:
        full_player_data = await ApiManager.getPlayerInfo(user.game_id)
        await redis_service.setex(key, ttl, str(full_player_data).encode())
        logger.info("Кэш создан")
    else:
        logger.info("Кэш получен")
        full_player_data = eval(cash_data)

    player_data = reformat_player_data(full_player_data)
    player_data["userPhotoUrl"] = user.photo_url
    return player_data


@users_rt.get(
    "/me/stats",
    response_class=JSONResponse
)
async def my_stats(
        payload: dict = PayloadDep,
        user: UserScheme = UserDep
):
    logger.info(f"Payload: {payload}")
    full_battlelog_data = await ApiManager.getPlayerBattleLog(user.game_id)
    battlelog_data = reformat_battlelog_data(full_battlelog_data)

    return battlelog_data


@users_rt.get(
    "/profile",
    response_class=JSONResponse
)
async def profile(
        payload: dict = PayloadDep,
        user: UserScheme = UserDep,
):
    logger.info(f"Payload: {payload}")
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "photo_url": user.photo_url,
        "email": user.email,
        "game_id": user.game_id
    }


@users_rt.get(
    "/profile/info",
    response_class=JSONResponse
)
async def profile_full_info(
        payload: dict = PayloadDep,
        user: UserScheme = UserDep,
):
    logger.info(f"Payload: {payload}")
    return user
