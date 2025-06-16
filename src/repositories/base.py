from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    orm = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.orm)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.orm).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, schema: BaseModel):
        add_stmt = insert(self.orm).values(**schema.model_dump()).returning(self.orm)
        result = await self.session.execute(add_stmt)
        return result.scalars().one()

    async def edit(self, schema: BaseModel, **filter_by) -> None:
        update_stmt = update(self.orm).filter_by(**filter_by).values(**schema.model_dump())
        result = await self.session.execute(update_stmt)
        rowcount = result.rowcount

        if rowcount > 1:
            raise HTTPException(400, "объектов больше чем 1")
        elif rowcount < 1:
            raise HTTPException(404, "объект не найден")

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.orm).filter_by(**filter_by)
        result = await self.session.execute(delete_stmt)
        rowcount = result.rowcount

        if rowcount < 1:
            raise HTTPException(404, "объект не найден")
