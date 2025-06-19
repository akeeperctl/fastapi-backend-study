from fastapi import APIRouter, HTTPException, Response, Request

from src.api.dependencies import UserIdDep
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAddScheme, UserAddScheme
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/login")
async def login_user(
        data: UserRequestAddScheme,
        response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_pwd(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail={"msg": "Пользователь с таким email не существует"})
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=403, detail={"msg": "Неверный пароль"})

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.post("/register")
async def register_user(
        data: UserRequestAddScheme
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAddScheme(email=data.email, hashed_password=hashed_password)

    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "ok"}


@router.post("/logout")
async def logout_user(
        response: Response
):
    response.delete_cookie("access_token")
    return {"status": "ok"}


@router.get("/me")
async def get_me(
        user_id: UserIdDep
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return {"data": user}
