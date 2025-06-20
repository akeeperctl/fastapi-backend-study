from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.schemas.bookings import BookingSchema


class BookingsRepository(BaseRepository):
    schema = BookingSchema
    orm = BookingsOrm
