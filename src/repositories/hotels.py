from sqlalchemy import select

from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ):
        query = select(self.model)
        if title:
            query = query.where(self.model.title.icontains(title.strip()))
        if location:
            query = query.where(self.model.location.icontains(location.strip()))

        query = (
            query
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(query)

        return result.scalars().all()
