from typing import Optional

from pydantic import BaseModel

from src.schemas.facilities import FacilitySchema
from src.pydantic_types import EntityId, UnsignedInt, EntityIdList


class RoomAddSchema(BaseModel):
    hotel_id: EntityId
    title: str
    description: Optional[str] = None
    price: UnsignedInt
    quantity: UnsignedInt


class RoomAddRequestSchema(BaseModel):
    title: str
    description: Optional[str] = None
    price: UnsignedInt
    quantity: UnsignedInt
    facilities_ids: EntityIdList = None


class RoomPatchRequestSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[UnsignedInt] = None  # Стоимость за ночь
    quantity: Optional[UnsignedInt] = None  # Количество номеров
    facilities_ids: Optional[EntityIdList] = None  # Идентификаторы удобств, добавляемые в номер


class RoomPatchSchema(BaseModel):
    hotel_id: Optional[EntityId] = None
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[UnsignedInt] = None
    quantity: Optional[UnsignedInt] = None


class RoomSchema(BaseModel):
    id: EntityId
    hotel_id: EntityId
    title: str
    description: Optional[str] = None
    price: UnsignedInt
    quantity: UnsignedInt


class RoomWithRelsSchema(RoomSchema):
    facilities: list[FacilitySchema]
