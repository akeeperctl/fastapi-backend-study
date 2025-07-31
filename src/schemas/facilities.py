from pydantic import BaseModel, Field

from src.pydantic_types import EntityId


class FacilityAddSchema(BaseModel):
    title: str = Field(min_length=3)


class FacilitySchema(FacilityAddSchema):
    id: EntityId


class RoomFacilityAddSchema(BaseModel):
    room_id: EntityId
    facility_id: EntityId


class RoomFacilitySchema(RoomFacilityAddSchema):
    id: EntityId
