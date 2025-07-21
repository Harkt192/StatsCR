from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse

from core.db import SessionDep
from users.schemes import UserGetScheme, UserCreateScheme, UserUpdateScheme
from users.service import UserService

users_rt = APIRouter(prefix="/users")


@users_rt.get("", response_class=JSONResponse)
async def get_users(session_dep: SessionDep):
    users = await UserService.get_all(session=session_dep)
    return users


@users_rt.post("/create", response_class=JSONResponse)
async def create_user(user_data: UserCreateScheme, session_dep: SessionDep):
    user = await UserService.create(user_data=user_data, session=session_dep)
    return user


@users_rt.get("/{user_id}", response_class=JSONResponse)
async def get_user_by_id(user_id: int, session_dep: SessionDep) -> UserGetScheme:
    user = await UserService.get(user_id=user_id, session=session_dep)
    if not user:
        return HTTPException(404, "Пользователь не найден")
    return user


@users_rt.patch("/change", response_class=JSONResponse)
async def update_user(user_data: UserGetScheme, session_dep: SessionDep):
    user = await UserService.update(user_data=user_data, session=session_dep)
    return user

