from datetime import date
from typing import Optional

from sqlalchemy import select, func, and_
from sqlalchemy.orm import aliased

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


def rooms_ids_for_bookings(
        date_from: date,
        date_to: date,
        hotel_id: Optional[int] = None,
):
    b = aliased(BookingsOrm)

    rooms_count = (
        select(
            b.room_id,
            func.count("*").label("rooms_booked")
        )
        .select_from(b)
        .where(and_(
            b.date_from <= date_to,
            b.date_to >= date_from
        ))
        .group_by(b.room_id)
        .order_by(b.room_id)
        .cte("rooms_count")
    )

    rooms_available_table = (
        select(
            RoomsOrm.id.label("room_id"),
            RoomsOrm.hotel_id,
            RoomsOrm.quantity,
            rooms_count.c.rooms_booked,
            (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_available"),
        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
        .cte("rooms_available_table")
    )

    rooms_ids_for_hotel = (
        select(RoomsOrm.id)
        .select_from(RoomsOrm)
    )

    if hotel_id is not None:
        rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)
    rooms_ids_for_hotel.subquery("rooms_ids_for_hotel")

    rooms_ids_to_get = (
        select(rooms_available_table.c.room_id)
        .select_from(rooms_available_table)
        .where(and_(
            rooms_available_table.c.rooms_available > 0,
            rooms_available_table.c.room_id.in_(rooms_ids_for_hotel)
        ))
    )

    # print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

    return rooms_ids_to_get
