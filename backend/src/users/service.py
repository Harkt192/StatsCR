from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User
from users.schemes import UserCreateScheme


class UserManager:
    @staticmethod
    async def get(*, user_id: int, session: AsyncSession):
        user = await session.get(User, user_id)
        return user

    @staticmethod
    async def put(*, user_data: UserCreateScheme, session: AsyncSession):
        user = User()
        query = update(User).where(User.id == changed_user.id).values(user)