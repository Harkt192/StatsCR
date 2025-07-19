from sqlalchemy import select, update, delete, text
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User
from users.schemes import UserCreateScheme, UserGetScheme

from core.db import SessionDep


class UserService:

    @staticmethod
    async def get_all(session: AsyncSession):
        print("get all")
        query = select(User)
        print(type(query), query)
        users = await session.execute(query)
        print(users)
        return users.scalars().all()


    @staticmethod
    async def get(*, user_id: int, session: AsyncSession) -> User or None:
        user = await session.get(User, user_id)
        return user

    @staticmethod
    async def create(*, user_data: UserCreateScheme, session: AsyncSession):
        session.add(user_data)
        result = await session.commit()
        return result   

    @staticmethod
    async def update(*, user_data: UserGetScheme, session: AsyncSession):
        # user = User(
        #     id=user_data.id,
        #     email=user_data.email,
        #     password=User.hash_password(user_data.password),
        #     first_name=user_data.first_name,
        #     last_name=user_data.last_name,
        #     game_id=user_data.game_id,
        #     language=user_data.language,
        #     photo_url=user_data.photo_url,
        #     active=user_data.active
        # )
        query = update(User).where(User.id == changed_user.id).values(user_data)
        result = await session.execute(query)
        return result

    @staticmethod
    async def deactivate(*, user_id: int, session: AsyncSession):
        query = update(User).where(User.id == user_id).values(User.active == False)
        result = await session.execute(query)
        return result

    @staticmethod
    async def activate(*, user_id: int, session: AsyncSession):
        query = update(User).where(User.id == user_id).values(User.active == True)
        result = await session.execute(query)
        return result

    @staticmethod
    async def delete(*, user_id: int, session: AsyncSession):
        query = delete(User).where(User.id == user_id)
        result = await session.execute(query)
        return result



UserService = UserService()

