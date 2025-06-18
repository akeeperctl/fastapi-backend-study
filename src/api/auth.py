from datetime import datetime, timezone, timedelta
from typing import Optional

import jwt
from fastapi import APIRouter, HTTPException, Response
from passlib.context import CryptContext

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAddScheme, UserAddScheme

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"  # алгоритм создания токена
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # сколько токен будет жить в минутах


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/login")
async def login_user(
        data: UserRequestAddScheme,
        response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_pwd(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail={"msg": "пользователь с таким email не существует"})
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=403, detail={"msg": "неверный пароль"})

        access_token = create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.post("/register")
async def register_user(
        data: UserRequestAddScheme
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAddScheme(email=data.email, hashed_password=hashed_password)

    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "ok"}
