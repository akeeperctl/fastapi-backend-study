from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddSchema, BookingAddRequestSchema

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", description="Забронировать комнату")
async def create_booking(
        user_id: UserIdDep,
        db: DBDep,
        data: BookingAddRequestSchema,
):
    room = await db.rooms.get_one_or_none(id=data.room_id)
    price_per_day = room.price
    days = (data.date_to - data.date_from).days
    final_price = price_per_day * days

    _data = BookingAddSchema(
        price=final_price,
        user_id=user_id,
        date_to=data.date_to,
        date_from=data.date_from,
        room_id=data.room_id
    )

    await db.bookings.add(_data)
    await db.commit()
    return {"statis": "ok", "data": _data}
