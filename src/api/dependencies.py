from typing import Optional, Annotated

from fastapi import Query, Depends
from pydantic import BaseModel


class PaginationParams(BaseModel):
    # Query - это тип Pydantic FieldInfo.
    page: Annotated[
        Optional[int], Query(default=1, ge=1, description="Номер страницы")]
    per_page: Annotated[
        Optional[int], Query(default=None, ge=1, lt=100, description="Сколько отелей находится на одной странице")]


# FastAPI прокинь все параметры из Pydantic схемы PaginationParams как Query-параметры
PaginationDep = Annotated[PaginationParams, Depends()]
