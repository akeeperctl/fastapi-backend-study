from fastapi import APIRouter, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import (
    UserPasswordWrongException,
    UserPasswordWrongHTTPException,
    UserAlreadyExistsException,
    UserAlreadyExistsHTTPException,
)
from src.schemas.users import UserRequestAddSchema
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    return {"data": await db.users.get_one_or_none(id=user_id)}


@router.post("/login")
async def login_user(
    db: DBDep,
    data: UserRequestAddSchema,
    response: Response,
):
    try:
        access_token = await AuthService(db).login_user(data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException
    except UserPasswordWrongException:
        raise UserPasswordWrongHTTPException

    response.set_cookie("access_token", access_token)
    return {"status": "ok", "data": access_token}


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAddSchema):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException
    return {"status": "ok"}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "ok"}
