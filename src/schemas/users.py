from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRequestAddScheme(BaseModel):
    """Схема на фронтенд API для добавления пользователя"""
    email: EmailStr
    password: str


class UserAddScheme(BaseModel):
    """Схема для добавления в репозиторий и отправки пользователя в базу данных"""
    email: EmailStr
    hashed_password: str


class UserScheme(BaseModel):
    id: int
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    nick_name: Optional[str]


class UserWithHashedPwdScheme(UserScheme):
    hashed_password: str
