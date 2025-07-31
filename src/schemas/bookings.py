from datetime import date, datetime

from pydantic import BaseModel

from src.pydantic_types import EntityId, UnsignedInt


class BookingAddRequestSchema(BaseModel):
    room_id: EntityId
    date_from: date
    date_to: date


class BookingPatchRequestSchema(BaseModel):
    room_id: EntityId
    date_from: date
    date_to: date


class BookingAddSchema(BaseModel):
    user_id: EntityId
    price: UnsignedInt

    room_id: EntityId
    date_from: date
    date_to: date


class BookingSchema(BaseModel):
    id: EntityId

    user_id: EntityId
    price: UnsignedInt

    room_id: EntityId
    date_from: date
    date_to: date

    updated_at: datetime
    created_at: datetime
