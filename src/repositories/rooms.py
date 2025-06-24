from datetime import date

from sqlalchemy import select, func, and_
from sqlalchemy.orm import aliased

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import RoomSchema


class RoomsRepository(BaseRepository):
    orm = RoomsOrm
    schema = RoomSchema

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
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
            .filter_by(hotel_id=hotel_id)
            .subquery("rooms_ids_for_hotel")
        )

        rooms_ids_to_get = (
            select(rooms_available_table.c.room_id)
            .select_from(rooms_available_table)
            .where(and_(
                rooms_available_table.c.rooms_available > 0,
                rooms_available_table.c.room_id.in_(rooms_ids_for_hotel)
            ))
        )

        # print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
