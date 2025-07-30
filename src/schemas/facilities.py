from pydantic import BaseModel, Field


class FacilityAddSchema(BaseModel):
    title: str


class FacilitySchema(FacilityAddSchema):
    id: int


class RoomFacilityAddSchema(BaseModel):
    room_id: int
    facility_id: int = Field(gt=0)


class RoomFacilitySchema(RoomFacilityAddSchema):
    id: int
