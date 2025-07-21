from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import RoomNotExistException, EditedTooMatchRoomsException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    orm = None
    mapper = DataMapper

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        """Получить фильтрованные данные"""
        query = select(self.orm).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(item) for item in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        """Получить все данные"""
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        """Получить единицу данных"""
        query = select(self.orm).filter_by(**filter_by)
        result = await self.session.execute(query)
        item = result.scalars().one_or_none()
        if item is None:
            return None
        return self.mapper.map_to_domain_entity(item)

    async def add(self, data: BaseModel):
        """Добавить единицу данных"""
        add_stmt = insert(self.orm).values(**data.model_dump()).returning(self.orm)
        result = await self.session.execute(add_stmt)
        item = result.scalars().one()
        return self.mapper.map_to_domain_entity(item)

    async def add_bulk(self, data: list[BaseModel]):
        """Добавить множество данных"""
        add_stmt = insert(self.orm).values([item.model_dump() for item in data])
        await self.session.execute(add_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> int:
        update_stmt = (
            update(self.orm)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )

        result = await self.session.execute(update_stmt)
        rowcount: int = result.rowcount

        return rowcount


    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.orm).filter_by(**filter_by)
        result = await self.session.execute(delete_stmt)
        rowcount = result.rowcount

        if rowcount < 1:
            raise HTTPException(404, "Объект не найден")
