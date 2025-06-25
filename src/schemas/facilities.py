from pydantic import BaseModel


class FacilityAddSchema(BaseModel):
    title: str


class FacilitySchema(FacilityAddSchema):
    id: int


class RoomFacilityAddSchema(BaseModel):
    room_id: int
    facility_id: int


class RoomFacilitySchema(RoomFacilityAddSchema):
    id: int
