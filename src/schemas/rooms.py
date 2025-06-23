from typing import Optional

from pydantic import BaseModel, Field


class RoomAddSchema(BaseModel):
    hotel_id: int
    title: str
    description: Optional[str] = None
    price: int
    quantity: int


class RoomAddRequestSchema(BaseModel):
    title: str
    description: Optional[str] = None
    price: int
    quantity: int = Field(description="Количество комнат в номере или количество мест в номере?")


class RoomPatchRequestSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None


class RoomPatchSchema(RoomPatchRequestSchema):
    hotel_id: Optional[int] = None


class RoomSchema(RoomAddSchema):
    id: int
    hotel_id: int
