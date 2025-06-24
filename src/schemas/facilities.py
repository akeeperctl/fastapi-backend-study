from pydantic import BaseModel


class FacilitiesAddSchema(BaseModel):
    title: str


class FacilitiesSchema(FacilitiesAddSchema):
    id: int

