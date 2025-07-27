from typing import Annotated

from sqlalchemy import select, update, delete, text
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User
from users.schemes import UserCreateScheme, UserGetScheme, UserScheme
from typing import Annotated
from core.db import SessionDep

from log import logger
from users.utils import hash_password, validate_password


class UserService:
    @staticmethod
    async def get_all(session: AsyncSession):
        query = select(User)
        users = await session.execute(query)
        return users.scalars().all()

    @staticmethod
    async def get(*, user_id: int, session: AsyncSession) -> User or None:
        user = await session.get(User, user_id)
        return user

    @staticmethod
    async def create(*, user_data: UserCreateScheme, session: AsyncSession):
        user_data = dict(user_data)
        user_data["password"] = await hash_password(user_data["password"])
        user = User(**user_data)
        session.add(user)
        await session.commit()

    @staticmethod
    async def update(*, user_data: UserScheme, session: AsyncSession):
        user_data = dict(user_data)
        if "password" in user_data.keys():
            user_data["password"] = await hash_password(user_data["password"])

        user = await session.get(User, user_data["id"])

        for key, value in user_data.items():
            if value:
                setattr(user, key, value)

        await session.commit()

    @staticmethod
    async def deactivate(*, user_id: int, session: AsyncSession):
        user = await session.get(User, user_id)
        user.active = False
        await session.commit()

    @staticmethod
    async def activate(*, user_id: int, session: AsyncSession):
        user = await session.get(User, user_id)
        user.active = True
        await session.commit()


UserService = UserService()

