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
    price: int = Field(description="Стоимость за ночь")
    quantity: int = Field(description="Количество комнат в номере")
    facilities_ids: Optional[list[int]] = Field(default=None, description="Идентификаторы удобств, добавляемые в номер")


class RoomPatchRequestSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = Field(default=None, description="Стоимость за ночь")
    quantity: Optional[int] = Field(default=None, description="Количество комнат в номере")


class RoomPatchSchema(RoomPatchRequestSchema):
    hotel_id: Optional[int] = None


class RoomSchema(RoomAddSchema):
    id: int
    hotel_id: int
