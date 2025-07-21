from sqlalchemy import select

from src.exceptions import DateFromLaterThanDateToException, HotelNotExistException
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import rooms_ids_for_bookings


class HotelsRepository(BaseRepository):
    orm = HotelsOrm
    mapper = HotelDataMapper

    async def get_one_or_none(self, **filter_by):
        hotel = await super().get_one_or_none(**filter_by)
        if hotel is None:
            raise HotelNotExistException()
        return hotel

    async def get_filtered_by_time(self, date_from, date_to, location, title, limit, offset):
        if date_from > date_to:
            raise DateFromLaterThanDateToException()

        rooms_ids_to_get = rooms_ids_for_bookings(date_from, date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        if title is not None:
            hotels_ids_to_get = hotels_ids_to_get.filter(self.orm.title.icontains(title.strip()))

        if location is not None:
            hotels_ids_to_get = hotels_ids_to_get.filter(
                self.orm.location.icontains(location.strip())
            )

        hotels_ids_to_get = hotels_ids_to_get.limit(limit).offset(offset)

        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids_to_get))
