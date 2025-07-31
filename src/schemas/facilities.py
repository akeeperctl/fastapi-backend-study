from pydantic import BaseModel

from src.pydantic_types import EntityId


class FacilityAddSchema(BaseModel):
    title: str


class FacilitySchema(FacilityAddSchema):
    id: EntityId


class RoomFacilityAddSchema(BaseModel):
    room_id: EntityId
    facility_id: EntityId


class RoomFacilitySchema(RoomFacilityAddSchema):
    id: EntityId
