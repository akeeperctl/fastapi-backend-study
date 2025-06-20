from sqlalchemy import insert

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import RoomsSchema, RoomsAddSchema


class RoomsRepository(BaseRepository):
    orm = RoomsOrm
    schema = RoomsSchema

    async def add_by_hotel_id(self, hotel_id: int, data: RoomsAddSchema):
        add_stmt = (
            insert(self.orm)
            .values(hotel_id=hotel_id, **data.model_dump())
            .returning(self.orm))

        result = await self.session.execute(add_stmt)
        item = result.scalars().first()
        return self.schema.model_validate(item, from_attributes=True)
