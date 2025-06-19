from fastapi import HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.schemas.users import UserScheme, UserWithHashedPwdScheme


class UsersRepository(BaseRepository):
    orm = UsersOrm
    schema = UserScheme

    async def add(self, data: BaseModel):
        try:
            return await super().add(data)
        except IntegrityError:
            raise HTTPException(status_code=409, detail={"msg": "Такой пользователь уже существует"})

    async def get_user_with_hashed_pwd(self, email: EmailStr):
        query = select(self.orm).filter_by(email=email)
        result = await self.session.execute(query)
        item = result.scalars().one()
        return UserWithHashedPwdScheme.model_validate(item, from_attributes=True)
