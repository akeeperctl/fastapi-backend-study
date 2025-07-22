from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import ObjectAlreadyExistsException
from src.schemas.users import UserRequestAddSchema, UserAddSchema
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
    user = await db.users.get_user_with_hashed_pwd(email=data.email)
    if not user:
        raise HTTPException(
            status_code=409, detail={"msg": "Пользователь с таким email не существует"}
        )
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=403, detail={"msg": "Неверный пароль"})

    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAddSchema):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAddSchema(email=data.email, hashed_password=hashed_password)

    try:
        await db.users.add(new_user_data)
        await db.commit()
    except ObjectAlreadyExistsException:
        raise HTTPException(
            status_code=409, detail={"msg": "Пользователь с таким email не существует"}
        )
    return {"status": "ok"}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "ok"}
