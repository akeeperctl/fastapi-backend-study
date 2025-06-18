from pydantic import BaseModel


class UserRequestAddScheme(BaseModel):
    """Схема на фронтенд API для добавления пользователя"""
    email: str
    password: str


class UserAddScheme(BaseModel):
    """Схема для добавления в репозиторий и отправки пользователя в базу данных"""
    email: str
    hashed_password: str


class UserScheme(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    nick_name: str
