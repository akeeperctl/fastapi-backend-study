from typing import Optional, Annotated

from fastapi import Query, Depends, Request
from loguru import logger
from pydantic import BaseModel

from src.config import settings
from src.pydantic_types import EntityId
from src.database import async_session_maker
from src.exceptions import (
    AuthTokenErrorException,
    AuthTokenErrorHTTPException,
    UserNotDefinedException,
    AuthTokenNotFoundHTTPException, ServiceNotAvailableHTTPException,
)
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    # Query - это тип Pydantic FieldInfo.
    page: Annotated[Optional[int], Query(default=1, ge=1, description="Номер страницы")]
    per_page: Annotated[
        Optional[int],
        Query(default=None, ge=1, lt=100, description="Сколько отелей находится на одной странице"),
    ]


# FastAPI прокинь все параметры из Pydantic схемы PaginationParams как Query-параметры
PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise AuthTokenNotFoundHTTPException
    return token


def get_current_user_id(token: str = Depends(get_token)) -> EntityId:
    try:
        token_data = AuthService().decode_token(token)
        user_id: Optional[EntityId] = token_data.get("user_id", None)
        if not user_id:
            raise UserNotDefinedException
    except AuthTokenErrorException as e:
        raise AuthTokenErrorHTTPException from e

    return user_id


UserIdDep = Annotated[EntityId, Depends(get_current_user_id)]


async def get_db():
    if not settings.DB_AVAILABLE:
        logger.critical("БД недоступна! Проверьте соединение!")
        raise ServiceNotAvailableHTTPException

    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
