from datetime import date, datetime

from pydantic import BaseModel


class BookingAddRequestSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAddSchema(BookingAddRequestSchema):
    user_id: int
    price: int


class BookingSchema(BookingAddSchema):
    id: int

    updated_at: datetime
    created_at: datetime
