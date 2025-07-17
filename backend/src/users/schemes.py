from typing import Optional

from pydantic import BaseModel


class UserBaseScheme(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreateScheme(UserBaseScheme):
    email: str
    password: str
    game_id: str
    language: Optional[str] = "ru"
    photo_url: Optional[str] = None


class UserGetScheme(UserCreateScheme):
    id: int