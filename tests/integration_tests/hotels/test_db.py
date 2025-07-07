from datetime import date

from src.schemas.bookings import BookingAddSchema, BookingAddRequestSchema


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAddSchema(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=8, day=10),
        date_to=date(year=2025, month=8, day=20),
        price=100,
    )
    # create
    added_booking = await db.bookings.add(booking_data)

    # read
    read_booking = await db.bookings.get_one_or_none(id=added_booking.id)

    # update
    update_booking_data = BookingAddRequestSchema(
        room_id=room_id,
        date_from=date(year=2025, month=8, day=20),
        date_to=date(year=2025, month=8, day=25),
    )
    await db.bookings.edit(data=update_booking_data, id=read_booking.id)

    # delete
    await db.bookings.delete(id=read_booking.id)

    await db.commit()
