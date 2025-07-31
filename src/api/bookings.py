from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    BookingRoomNotAvailableException,
    BookingRoomNotAvailableHTTPException,
    DateFromLaterDateToException,
    DateFromLaterDateToHTTPException,
)
from src.schemas.bookings import BookingAddRequestSchema
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", description="Забронировать номер")
async def create_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequestSchema,
):
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except DateFromLaterDateToException as e:
        raise DateFromLaterDateToHTTPException from e
    except BookingRoomNotAvailableException as e:
        raise BookingRoomNotAvailableHTTPException from e

    return {"status": "ok", "data": booking}


@router.get("", description="Получить все бронирования")
async def get_bookings(db: DBDep):
    bookings = await BookingService(db).get_bookings()
    return {"status": "ok", "data": bookings}


@router.get("/me", description="Получить бронирования авторизованного пользователя")
async def get_me_bookings(user_id: UserIdDep, db: DBDep):
    bookings = await BookingService(db).get_me_bookings(user_id)
    return {"status": "ok", "data": bookings}
