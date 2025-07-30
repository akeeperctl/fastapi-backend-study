from typing import Optional

from pydantic import BaseModel, Field

from src.schemas.facilities import FacilitySchema


class RoomAddSchema(BaseModel):
    hotel_id: int
    title: str
    description: Optional[str] = None
    price: int = Field(gt=0)
    quantity: int = Field(gt=0)


class RoomAddRequestSchema(BaseModel):
    title: str
    description: Optional[str] = None
    price: int = Field(description="Стоимость за ночь", gt=0)
    quantity: int = Field(description="Количество комнат в номере", gt=0)
    facilities_ids: list[int] = Field(
        default=None, description="Идентификаторы удобств, добавляемые в номер"
    )


class RoomPatchRequestSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = Field(default=None, description="Стоимость за ночь", gt=0)
    quantity: Optional[int] = Field(default=None, description="Количество номеров", gt=0)
    facilities_ids: Optional[list[int]] = Field(
        default=None, description="Идентификаторы удобств, добавляемые в номер"
    )


class RoomPatchSchema(BaseModel):
    hotel_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = Field(default=None, gt=0)
    quantity: Optional[int] = Field(default=None, gt=0)


class RoomSchema(BaseModel):
    id: int
    hotel_id: int
    title: str
    description: Optional[str] = None
    price: int
    quantity: int


class RoomWithRelsSchema(RoomSchema):
    facilities: list[FacilitySchema]
