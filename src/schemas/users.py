from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRequestAddSchema(BaseModel):
    """Схема на фронтенд API для добавления пользователя"""
    email: EmailStr
    password: str


class UserAddSchema(BaseModel):
    """Схема для добавления в репозиторий и отправки пользователя в базу данных"""
    email: EmailStr
    hashed_password: str


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    nick_name: Optional[str]


class UserWithHashedPwdSchema(UserSchema):
    hashed_password: str
