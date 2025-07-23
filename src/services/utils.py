from datetime import date

from src.exceptions import (DateFromLaterDateToException, HotelNotFoundException, ObjectNotFoundException,
                            RoomNotFoundException)
from src.utils.db_manager import DBManager


class DataChecker:
    @staticmethod
    def _check_dates(date_from: date, date_to: date) -> None:
        if date_from >= date_to:
            raise DateFromLaterDateToException

    @staticmethod
    async def _check_hotel_available(db: DBManager, hotel_id: int) -> None:
        try:
            await db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as e:
            raise HotelNotFoundException from e

    @staticmethod
    async def _check_room_available(db: DBManager, room_id: int) -> None:
        try:
            await db.rooms.get_one(id=room_id)
        except ObjectNotFoundException as e:
            raise RoomNotFoundException from e

