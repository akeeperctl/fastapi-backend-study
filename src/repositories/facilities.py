from src.models.facilities import FacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import FacilitySchema


class FacilitiesRepository(BaseRepository):
    schema = FacilitySchema
    orm = FacilitiesOrm
