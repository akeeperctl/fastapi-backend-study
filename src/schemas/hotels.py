# Называют схемой данный, реже модель
# Представляет данные, их свойства, позволяет не нарушать DRY
from typing import Optional

from pydantic import BaseModel, ConfigDict


class HotelAddSchema(BaseModel):
    title: str
    location: str


# Схема соответствует объекту алхимии HotelOrm
class HotelSchema(HotelAddSchema):
    id: int


class HotelPatchSchema(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
