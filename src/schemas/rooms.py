from typing import Optional

from pydantic import BaseModel


class RoomsAddSchema(BaseModel):
    title: str
    description: Optional[str]
    price: int
    quantity: int


class RoomsPatchSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None


class RoomsSchema(RoomsAddSchema):
    id: int
    hotel_id: int
