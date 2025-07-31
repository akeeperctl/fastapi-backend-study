# Называют схемой данный, реже модель
# Представляет данные, их свойства, позволяет не нарушать DRY
from typing import Optional

from pydantic import BaseModel

from src.pydantic_types import EntityId


class HotelAddSchema(BaseModel):
    title: str  # Название отеля
    location: str  # Город, в котором находится отель


# Схема соответствует объекту алхимии HotelOrm
class HotelSchema(HotelAddSchema):
    id: EntityId


class HotelPatchSchema(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
