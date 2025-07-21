from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import BookingRoomNotAvailableException
from src.schemas.bookings import BookingAddSchema, BookingAddRequestSchema

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", description="Забронировать номер")
async def create_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequestSchema,
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Номер не найден")

    price_per_day = room.price
    days = max((booking_data.date_to - booking_data.date_from).days, 1)
    final_price = price_per_day * days

    _booking_data = BookingAddSchema(
        price=final_price, user_id=user_id, **booking_data.model_dump()
    )

    try:
        await db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
    except BookingRoomNotAvailableException:
        raise HTTPException(
            status_code=404, detail="Номер недоступен для бронирования на указанный срок"
        )

    await db.commit()
    return {"status": "ok", "data": _booking_data}


@router.get("", description="Получить все бронирования")
async def get_bookings(db: DBDep):
    return {"data": await db.bookings.get_all()}


@router.get("/me", description="Получить бронирования авторизованного пользователя")
async def get_me_bookings(user_id: UserIdDep, db: DBDep):
    return {"data": await db.bookings.get_filtered(user_id=user_id)}


# @router.delete("/{booking_id}", description="Удалить определенное бронирование")
# async def delete_booking(
#         db: DBDep,
#         booking_id: int
# ):
#     await db.bookings.delete(id=booking_id)
#     await db.commit()
#     return {"status": "ok"}
