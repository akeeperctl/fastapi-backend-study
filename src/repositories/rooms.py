from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_bookings
from src.schemas.rooms import RoomSchema, RoomWithRelsSchema


class RoomsRepository(BaseRepository):
    orm = RoomsOrm
    schema = RoomSchema

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        rooms_ids_to_get = rooms_ids_for_bookings(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

        query = (
            select(self.orm)
            .options(selectinload(self.orm.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        result = await self.session.execute(query)
        return [RoomWithRelsSchema.model_validate(orm, from_attributes=True) for orm in result.unique().scalars().all()]
