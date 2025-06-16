# Называют схемой данный, реже модель
# Представляет данные, их свойства, позволяет не нарушать DRY
from typing import Optional

from pydantic import BaseModel


class HotelSchema(BaseModel):
    title: str
    location: str


class HotelPatchSchema(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
