from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import ForeignKey, Integer, Text, String, Boolean
import bcrypt
from core.db import Base
from typing import Optional

from users.schemes import UserCreateScheme


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(200))
    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    game_id: Mapped[Optional[str]] = mapped_column(String(9), unique=True)
    language: Mapped[Optional[str]] = mapped_column(String(10), default="ru")
    photo_url: Mapped[Optional[str]] = mapped_column(String(200))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    @staticmethod
    async def hash_password(received_password: str) -> str:
        hashed_password = str(bcrypt.hashpw(received_password.encode(), bcrypt.gensalt()))
        return hashed_password

    async def check_password(self, received_password: str) -> bool:
        result = bcrypt.checkpw(received_password.encode(), self.password.encode())
        return result

    @staticmethod
    async def create_user_from_scheme(user_data: UserCreateScheme) -> User:
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password=await User.hash_password(user_data.password),
            game_id=user_data.game_id,
            language=user_data.language,
            photo_url=user_data.photo_url,
        )
        return user

    def __str__(self):
        return f"""<User[id={self.id};email={self.email}]>"""
