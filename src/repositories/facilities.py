from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import FacilitySchema, RoomFacilitySchema


class FacilitiesRepository(BaseRepository):
    schema = FacilitySchema
    orm = FacilitiesOrm


class RoomsFacilitiesRepository(BaseRepository):
    schema = RoomFacilitySchema
    orm = RoomsFacilitiesOrm
