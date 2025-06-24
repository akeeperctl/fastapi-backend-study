from pydantic import BaseModel


class FacilityAddSchema(BaseModel):
    title: str


class FacilitySchema(FacilityAddSchema):
    id: int

