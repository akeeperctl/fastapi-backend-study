from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashedPwdSchema


class UsersRepository(BaseRepository):
    orm = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_pwd(self, email: EmailStr):
        query = select(self.orm).filter_by(email=email)
        result = await self.session.execute(query)
        item = result.scalars().one_or_none()
        if item:
            return UserWithHashedPwdSchema.model_validate(item, from_attributes=True)
        return None
