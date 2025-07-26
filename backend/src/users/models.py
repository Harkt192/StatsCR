from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import ForeignKey, Integer, Text, String, Boolean
import bcrypt
from core.db import Base
from typing import Optional


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
        hashed_password = bcrypt.hashpw(received_password.encode(), bcrypt.gensalt()).decode()
        return hashed_password

    async def check_password(self, received_password: str) -> bool:
        result = bcrypt.checkpw(received_password.encode(), self.password.encode())
        return result

    def __str__(self):
        return f"""<User[id={self.id};email={self.email}]>"""

    def __repr__(self):
        return f"""[{self.id} {self.email} {self.game_id}]"""
