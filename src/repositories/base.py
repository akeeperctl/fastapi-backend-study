from pydantic import BaseModel
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import engine


class BaseRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, schema: BaseModel):
        add_stmt = insert(self.model).values(**schema.model_dump()).returning(self.model)
        print(f"add_stmt={add_stmt.compile(engine, compile_kwargs={'literal_binds': True})}")
        return await self.session.execute(add_stmt)

    async def commit(self):
        return await self.session.commit()


