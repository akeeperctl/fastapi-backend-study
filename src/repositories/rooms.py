from datetime import date

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.exceptions import DateFromLaterThanDateToException, RoomNotExistException, EditedTooMatchRoomsException
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper
from src.repositories.utils import rooms_ids_for_bookings
from src.schemas.rooms import RoomWithRelsSchema


class RoomsRepository(BaseRepository):
    orm = RoomsOrm
    mapper = RoomDataMapper

    async def add(self, data: BaseModel):
        await super().add(data)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        row_count = await super().edit(data, exclude_unset=exclude_unset, **filter_by)
        if row_count > 1:
            raise EditedTooMatchRoomsException()
        elif row_count < 1:
            raise RoomNotExistException()

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        """Получение свободных номеров, в указанный промежуток времени"""
        if date_from > date_to:
            raise DateFromLaterThanDateToException()

        rooms_ids_to_get = rooms_ids_for_bookings(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

        query = (
            select(self.orm)
            .options(selectinload(self.orm.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        result = await self.session.execute(query)
        return [
            RoomWithRelsSchema.model_validate(orm, from_attributes=True)
            for orm in result.unique().scalars().all()
        ]

    async def get_one_or_none_with_rels(self, **filter_by):
        """Получение номера с загрузкой зависимостей"""
        query = select(self.orm).options(selectinload(self.orm.facilities)).filter_by(**filter_by)
        result = await self.session.execute(query)
        item = result.scalars().one_or_none()

        if item is None:
            raise RoomNotExistException()

        return RoomWithRelsSchema.model_validate(item, from_attributes=True)

    async def get_one_or_none(self, **filter_by):
        item = await super().get_one_or_none(**filter_by)
        if item is None:
            raise RoomNotExistException()
        return item
