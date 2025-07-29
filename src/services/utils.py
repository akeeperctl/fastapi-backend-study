from datetime import date

from src.exceptions import (
    DateFromLaterDateToException,
    HotelNotFoundException,
    ObjectNotFoundException,
    RoomNotFoundException, )
from src.schemas.hotels import HotelSchema
from src.schemas.rooms import RoomSchema
from src.utils.db_manager import DBManager


class DataChecker:
    @staticmethod
    def _check_dates(date_from: date, date_to: date) -> None:
        if date_from >= date_to:
            raise DateFromLaterDateToException

    @staticmethod
    async def _check_and_get_hotel(db: DBManager, hotel_id: int) -> HotelSchema:
        try:
            hotel = await db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as e:
            raise HotelNotFoundException from e
        return hotel

    @staticmethod
    async def _check_and_get_room(db: DBManager, room_id: int) -> RoomSchema:
        try:
            room = await db.rooms.get_one(id=room_id)
        except ObjectNotFoundException as e:
            raise RoomNotFoundException from e
        return room

    @staticmethod
    async def _check_and_replace_facilities(db: DBManager, room_id: int, room_data: dict) -> None:
        facilities_ids = room_data.get("facilities_ids", None)
        if facilities_ids:
            await db.rooms_facilities.replace_facilities(
                room_id=room_id, facilities_ids=facilities_ids
            )
