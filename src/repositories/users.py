from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.schemas.users import UserScheme


class UsersRepository(BaseRepository):
    orm = UsersOrm
    schema = UserScheme

    async def add(self, data: BaseModel):
        try:
            return await super().add(data)
        except IntegrityError:
            raise HTTPException(status_code=409, detail={"msg": "такой пользователь уже существует"})
