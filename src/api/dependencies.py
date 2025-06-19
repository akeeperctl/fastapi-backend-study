from typing import Optional, Annotated

from fastapi import Query, Depends, Request, HTTPException
from pydantic import BaseModel

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    # Query - это тип Pydantic FieldInfo.
    page: Annotated[
        Optional[int], Query(default=1, ge=1, description="Номер страницы")]
    per_page: Annotated[
        Optional[int], Query(default=None, ge=1, lt=100, description="Сколько отелей находится на одной странице")]


# FastAPI прокинь все параметры из Pydantic схемы PaginationParams как Query-параметры
PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail={"msg": "Вы не предоставили токен доступа"})
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    token_data = AuthService().decode_token(token)
    return token_data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]
