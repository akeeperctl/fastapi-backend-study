from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.exceptions import RoomNotFoundException
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomWithRelsDataMapper
from src.repositories.utils import rooms_ids_for_bookings


class RoomsRepository(BaseRepository):
    orm = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        """Получение свободных номеров, в указанный промежуток времени"""

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
            self.mapper.map_to_domain_entity(orm)
            for orm in result.unique().scalars().all()
        ]

    async def get_one_with_rels(self, **filter_by):
        """Получение номера с загрузкой зависимостей"""
        query = select(self.orm).options(selectinload(self.orm.facilities)).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            item = result.scalars().one()
        except NoResultFound:
            raise RoomNotFoundException

        return RoomWithRelsDataMapper.map_to_domain_entity(item)
