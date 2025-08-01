from asyncpg import ForeignKeyViolationError
from loguru import logger
from sqlalchemy import select, insert, delete, exists
from sqlalchemy.exc import IntegrityError

from src.exceptions import FacilityKeyNotCorrectException
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper, RoomsFacilityDataMapper


class FacilitiesRepository(BaseRepository):
    orm = FacilitiesOrm
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    orm = RoomsFacilitiesOrm
    mapper = RoomsFacilityDataMapper

    async def replace_facilities(
        self,
        room_id: int,
        facilities_ids: list[int],
    ):
        """Заменить список идентификаторов удобств в указанной комнате"""

        """
        facilities_ids = [1,2,4]
        current_facilities_ids = [1,3]
        facilities_ids_to_add = [facilities_ids - current_facilities_ids]
        facilities_ids_to_delete = [current_facilities_ids - facilities_ids]
        current_facilities_ids = [1,2,4]
        """

        current_facilities_ids_q = (
            select(self.orm.facility_id).select_from(self.orm).where(self.orm.room_id == room_id)
        )
        result = await self.session.execute(current_facilities_ids_q)
        current_facilities_ids = result.scalars().all()

        # Получение идентификаторов путем вычитания множеств
        facilities_ids_to_add = [
            {
                "room_id": room_id,
                "facility_id": f_id,
            }
            for f_id in (set(facilities_ids) - set(current_facilities_ids))
        ]

        facilities_ids_to_delete = set(current_facilities_ids) - set(facilities_ids)

        if facilities_ids_to_add or facilities_ids_to_delete:
            stmt = select(self.orm).select_from(self.orm).where(self.orm.room_id == room_id)

            if facilities_ids_to_add:
                facilities_add_ids = (
                    insert(self.orm)
                    .values(facilities_ids_to_add)
                    .returning(self.orm.facility_id)
                    .cte("facilities_add_ids")
                )

                stmt = stmt.where(exists(select(1).select_from(facilities_add_ids)))

            if facilities_ids_to_delete:
                facilities_delete_ids = (
                    delete(self.orm)
                    .where(
                        self.orm.facility_id.in_(facilities_ids_to_delete),
                        self.orm.room_id == room_id,
                    )
                    .returning(self.orm.facility_id)
                    .cte("facilities_delete_ids")
                )
                stmt = stmt.where(exists(select(1).select_from(facilities_delete_ids)))

            try:
                await self.session.execute(stmt)
            except IntegrityError as e:
                logger.error(
                    f"Не удалось заменить удобства в БД, тип ошибки: {type(e.orig.__cause__)=}"
                )
                if isinstance(e.orig.__cause__, ForeignKeyViolationError):
                    raise FacilityKeyNotCorrectException from e
                else:
                    logger.error(f"Незнакомая ошибка, тип ошибки: {type(e.orig.__cause__)=}")
                    raise e
