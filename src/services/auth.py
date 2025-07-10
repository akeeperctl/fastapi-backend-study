from datetime import datetime, timezone, timedelta

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from src.config import settings


class AuthService:
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
        except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
            raise HTTPException(status_code=401, detail={"msg": "Неверный токен"})
