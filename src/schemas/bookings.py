from datetime import datetime

from pydantic import BaseModel


class BookingAddRequestSchema(BaseModel):
    room_id: int
    date_from: datetime
    date_to: datetime


class BookingAddSchema(BookingAddRequestSchema):
    user_id: int
    price: int


class BookingSchema(BookingAddSchema):
    id: int
