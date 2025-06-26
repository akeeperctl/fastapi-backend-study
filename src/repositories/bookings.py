from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    orm = BookingsOrm
    mapper = BookingDataMapper
