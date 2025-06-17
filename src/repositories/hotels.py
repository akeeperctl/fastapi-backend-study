from sqlalchemy import select

from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from src.schemas.hotels import HotelSchema


class HotelsRepository(BaseRepository):
    orm = HotelsOrm
    schema = HotelSchema

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ):
        query = select(self.orm)
        if title:
            query = query.where(self.orm.title.icontains(title.strip()))
        if location:
            query = query.where(self.orm.location.icontains(location.strip()))

        query = (
            query
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(query)
        return [self.schema.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
