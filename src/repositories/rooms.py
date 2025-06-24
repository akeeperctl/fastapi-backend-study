from datetime import date

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_bookings
from src.schemas.rooms import RoomSchema


class RoomsRepository(BaseRepository):
    orm = RoomsOrm
    schema = RoomSchema

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date
    ):

        rooms_ids_to_get = rooms_ids_for_bookings(date_from=date_from, date_to=date_to)

        # print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
