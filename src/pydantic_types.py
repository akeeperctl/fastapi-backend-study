"""Общие типы переменных на основе валидации pydantic'а"""

from typing import Annotated

from pydantic.fields import Field

UnsignedInt = Annotated[int, Field(gt=0)]
EntityId = UnsignedInt
EntityIdList = list[EntityId]
