from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    orm = None
    schema: BaseModel = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.orm)
            .filter(*filter)
            .filter_by(**filter_by))
        result = await self.session.execute(query)

        # model_validate валидирует что объект "hotel" соответствует схеме Pydantic HotelSchema
        # from_attributes=True заставляет Pydantic валидировать объект по его атрибутам
        return [self.schema.model_validate(item, from_attributes=True) for item in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.orm).filter_by(**filter_by)
        result = await self.session.execute(query)
        item = result.scalars().one_or_none()

        if item is None:
            return None
        return self.schema.model_validate(item, from_attributes=True)

    async def add(self, data: BaseModel):
        """Добавить единицу данных"""
        add_stmt = insert(self.orm).values(**data.model_dump()).returning(self.orm)
        result = await self.session.execute(add_stmt)
        return self.schema.model_validate(result.scalars().one(), from_attributes=True)

    async def add_bulk(self, data: list[BaseModel]):
        """Добавить множество данных"""
        add_stmt = insert(self.orm).values([item.model_dump() for item in data])
        await self.session.execute(add_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.orm).
            filter_by(**filter_by).
            values(**data.model_dump(exclude_unset=exclude_unset))
        )

        result = await self.session.execute(update_stmt)
        rowcount = result.rowcount

        if rowcount > 1:
            raise HTTPException(400, "Объектов больше чем 1")
        elif rowcount < 1:
            raise HTTPException(404, "Объект не найден")

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.orm).filter_by(**filter_by)
        result = await self.session.execute(delete_stmt)
        rowcount = result.rowcount

        if rowcount < 1:
            raise HTTPException(404, "Объект не найден")
