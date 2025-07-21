from typing import Optional

from pydantic import BaseModel


class UserBaseScheme(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreateScheme(UserBaseScheme):
    email: str
    password: str
    game_id: str
    language: Optional[str] = "ru"
    photo_url: Optional[str] = None


class UserGetScheme(UserCreateScheme):
    id: int


class UserUpdateScheme(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    game_id: Optional[str] = None
    language: Optional[str] = None
    photo_url: Optional[str] = None
    active: Optional[bool] = None

