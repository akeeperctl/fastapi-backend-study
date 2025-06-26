from typing import TypeVar

from pydantic import BaseModel

from src.database import Base

DBOrmType = TypeVar('DBOrmType', bound=Base)
SchemaType = TypeVar('SchemaType', bound=BaseModel)


class DataMapper:
    orm: type[DBOrmType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, data):
        # model_validate валидирует что объект "hotel" соответствует схеме Pydantic HotelSchema
        # from_attributes=True заставляет Pydantic валидировать объект по его атрибутам
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.orm(**data.model_dump())
