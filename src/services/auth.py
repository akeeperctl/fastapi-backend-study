from datetime import datetime, timezone, timedelta

import jwt
from passlib.context import CryptContext

from src.config import settings
from src.exceptions import (AuthTokenErrorException, ObjectAlreadyExistsException, UserAlreadyExistsException,
                            UserPasswordWrongException)
from src.schemas.users import UserRequestAddSchema, UserAddSchema
from src.services.base import BaseService


class AuthService(BaseService):
    """Вся история связанная с авторизацией"""

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def decode_token(encoded_token: str) -> dict:
        try:
            return jwt.decode(
                encoded_token, key=settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM
            )
        except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError) as e:
            raise AuthTokenErrorException from e
        
    async def login_user(self, data: UserRequestAddSchema):
        user = await self.db.users.get_user_with_hashed_pwd(email=data.email)
        if not user:
            raise UserAlreadyExistsException
        if not self.verify_password(data.password, user.hashed_password):
            raise UserPasswordWrongException
        
        access_token = self.create_access_token({"user_id": user.id})
        return access_token

    async def register_user(self, data: UserRequestAddSchema):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAddSchema(email=data.email, hashed_password=hashed_password)

        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise UserAlreadyExistsException
