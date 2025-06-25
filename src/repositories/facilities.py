from typing import Optional

from sqlalchemy import select, and_, insert, delete, exists

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import FacilitySchema, RoomFacilitySchema, RoomFacilityAddSchema


class FacilitiesRepository(BaseRepository):
    schema = FacilitySchema
    orm = FacilitiesOrm


class RoomsFacilitiesRepository(BaseRepository):
    schema = RoomFacilitySchema
    orm = RoomsFacilitiesOrm

    async def replace_facilities(
            self,
            room_id: int,
            facilities_ids: Optional[list[int]],
    ):
        if facilities_ids is None:
            return

        # facilities_ids = [1,4]
        # db = [1,4]
        # facilities_ids_to_save = [1,4]
        # facilities_ids_to_add = []
        # facilities_ids_to_delete = []
        # db = [1,4]

        room_facilities_ids_q = (
            select(self.orm.facility_id)
            .select_from(self.orm)
            .where(and_(
                self.orm.room_id == room_id,
            ))
        )
        result = await self.session.execute(room_facilities_ids_q)
        room_facilities_ids = result.scalars().all()

        facilities_ids_to_save = [f_id for f_id in facilities_ids if f_id in room_facilities_ids]
        facilities_ids_to_delete = [f_id for f_id in room_facilities_ids if f_id not in facilities_ids_to_save]
        facilities_ids_to_add = [
            RoomFacilityAddSchema(room_id=room_id, facility_id=f_id).model_dump()
            for f_id in facilities_ids if f_id not in room_facilities_ids
        ]

        facilities_add_ids = (
            insert(self.orm)
            .values(facilities_ids_to_add)
            .returning(self.orm.facility_id)
            .cte("facilities_add_ids")
        )

        facilities_delete_ids = (
            delete(self.orm)
            .where(self.orm.facility_id.in_(facilities_ids_to_delete))
            .returning(self.orm.facility_id)
            .cte("facilities_delete_ids")
        )

        stmt = (
            select(self.orm)
            .select_from(self.orm)
            .where(self.orm.room_id == room_id)
        )

        if facilities_ids_to_add:
            stmt = stmt.where(exists(select(1).select_from(facilities_add_ids)))

        if facilities_ids_to_delete:
            stmt = stmt.where(exists(select(1).select_from(facilities_delete_ids)))

        # print(stmt.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        await self.session.execute(stmt)

        # remaining = [self.schema.model_validate(item, from_attributes=True) for item in result.scalars().all()]
        # print(f"{remaining=}")
