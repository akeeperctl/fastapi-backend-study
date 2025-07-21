from datetime import date

from sqlalchemy import select, and_

from src.models import RoomsOrm
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.exceptions import BookingRoomNotAvailableException
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_bookings
from src.schemas.bookings import BookingAddSchema


class BookingsRepository(BaseRepository):
    orm = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())

        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, data: BookingAddSchema, hotel_id: int):
        """Добавить бронирование, если номер доступен для бронирования"""

        rooms_ids_for_bookings_q = rooms_ids_for_bookings(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id,
        )

        query = select(RoomsOrm).filter(
            and_(
                RoomsOrm.id == data.room_id,
                RoomsOrm.id.in_(rooms_ids_for_bookings_q),
            )
        )

        result = await self.session.execute(query)
        room_data = result.scalars().one_or_none()
        if not room_data:
            raise BookingRoomNotAvailableException(
                "Номер недоступна для бронирования на указанный срок"
            )

        added_booking = await super().add(data)
        return added_booking
