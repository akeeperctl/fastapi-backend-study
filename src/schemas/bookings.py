from datetime import date, datetime

from pydantic import BaseModel


class BookingAddRequestSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingPatchRequestSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAddSchema(BaseModel):
    user_id: int
    price: int

    room_id: int
    date_from: date
    date_to: date


class BookingSchema(BaseModel):
    id: int

    user_id: int
    price: int

    room_id: int
    date_from: date
    date_to: date

    updated_at: datetime
    created_at: datetime
