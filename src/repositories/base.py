from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import (ObjectAlreadyExistsException, ObjectNotFoundException, ObjectKeyNotCorrectException)
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

    async def get_one(self, **filter_by):
        """Получить единицу данных"""
        query = select(self.orm).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            item = result.scalars().one()
        except NoResultFound as e:
            logger.error(f"Не удалось получить данные из БД, тип ошибки: {type(e)=}")
            raise ObjectNotFoundException from e
        return self.mapper.map_to_domain_entity(item)

    async def add(self, data: BaseModel):
        """Добавить единицу данных"""

        try:
            add_stmt = insert(self.orm).values(**data.model_dump()).returning(self.orm)
            result = await self.session.execute(add_stmt)
            item = result.scalars().one()
        except IntegrityError as e:
            logger.error(f"Не удалось добавить данные в БД, тип ошибки: {type(e.orig.__cause__)=}")
            if isinstance(e.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from e
            else:
                logger.error(f"Незнакомая ошибка, тип ошибки: {type(e.orig.__cause__)=}")
                raise e

        return self.mapper.map_to_domain_entity(item)

    async def add_bulk(self, data: list[BaseModel]):
        """Добавить множество данных"""

        try:
            add_stmt = insert(self.orm).values([item.model_dump() for item in data])
            await self.session.execute(add_stmt)
        except IntegrityError as e:
            logger.error(f"Не удалось добавить данные в БД, тип ошибки: {type(e.orig.__cause__)=}")
            if isinstance(e.orig.__cause__, ForeignKeyViolationError):
                raise ObjectKeyNotCorrectException from e
            else:
                logger.error(f"Незнакомая ошибка, тип ошибки: {type(e.orig.__cause__)=}")
                raise e

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        update_stmt = (
            update(self.orm)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )

        await self.session.execute(update_stmt)
        # rowcount: int = result.rowcount
        #
        # if rowcount > 1:
        #     raise EditedTooMatchObjects
        # elif rowcount < 1:
        #     raise ObjectNotFoundException

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.orm).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
        # rowcount = result.rowcount
        #
        # if rowcount < 1:
        #     raise ObjectNotFoundException
