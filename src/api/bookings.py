from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddSchema, BookingAddRequestSchema

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", description="Забронировать комнату")
async def create_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequestSchema,
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    price_per_day = room.price
    days = (booking_data.date_to - booking_data.date_from).days
    final_price = price_per_day * days

    _booking_data = BookingAddSchema(
        price=final_price,
        user_id=user_id,
        **booking_data.model_dump()
    )

    await db.bookings.add(_booking_data)
    await db.commit()
    return {"statis": "ok", "data": _booking_data}
