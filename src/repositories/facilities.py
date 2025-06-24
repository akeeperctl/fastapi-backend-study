from src.models.facilities import FacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import FacilitiesSchema


class FacilitiesRepository(BaseRepository):
    schema = FacilitiesSchema
    orm = FacilitiesOrm
