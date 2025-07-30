from datetime import date

from src.exceptions import ObjectKeyNotCorrectException, FacilityKeyNotCorrectException
from src.schemas.facilities import RoomFacilityAddSchema
from src.schemas.rooms import (
    RoomAddSchema,
    RoomAddRequestSchema,
    RoomPatchRequestSchema,
    RoomPatchSchema,
)
from src.services.base import BaseService
from src.services.utils import DataChecker


class RoomService(BaseService, DataChecker):
    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        """Получить номера отеля, отфильтрованные по времени заезда и выезда"""

        self._check_dates(date_from, date_to)
        await self._check_and_get_hotel(self.db, hotel_id)

        rooms = await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
        return rooms

    async def get_room(self, room_id: int, hotel_id: int):
        """Получить данные номера по его идентификатору и идентификатору отеля"""

        await self._check_and_get_hotel(self.db, hotel_id)
        room = await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)
        return room

    async def create_room(self, room_data: RoomAddRequestSchema, hotel_id: int):
        """Создать номер в отеле"""

        await self._check_and_get_hotel(self.db, hotel_id)

        _room_data = RoomAddSchema(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(_room_data)

        if room_data.facilities_ids:
            if 0 in room_data.facilities_ids:
                raise FacilityKeyNotCorrectException

            room_facilities_data = [
                RoomFacilityAddSchema(room_id=room.id, facility_id=f_id)
                for f_id in room_data.facilities_ids
            ]

            try:
                await self.db.rooms_facilities.add_bulk(room_facilities_data)
            except ObjectKeyNotCorrectException as e:
                raise FacilityKeyNotCorrectException from e

        await self.db.commit()
        return room

    async def edit_room(self, hotel_id: int, room_id: int, room_data: RoomAddRequestSchema) -> None:
        """Полное редактирование номера"""

        await self._check_and_get_hotel(self.db, hotel_id)
        await self._check_and_get_room(self.db, room_id)

        _room_data_dict = room_data.model_dump()
        _room_data = RoomAddSchema(hotel_id=hotel_id, **_room_data_dict)

        await self.db.rooms.edit(data=_room_data, id=room_id, hotel_id=hotel_id)
        await self._check_and_replace_facilities(self.db, room_id, _room_data_dict)
        await self.db.commit()

    async def patch_room(self, hotel_id: int, room_id: int, room_data: RoomPatchRequestSchema):
        """Частичное редактирование номера"""

        await self._check_and_get_hotel(self.db, hotel_id)
        await self._check_and_get_room(self.db, room_id)

        # exclude_unset=True отбрасывает неуказанные свойства для изменения
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatchSchema(hotel_id=hotel_id, **_room_data_dict)

        await self.db.rooms.edit(data=_room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
        await self._check_and_replace_facilities(self.db, room_id, _room_data_dict)
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        """Удалить номер из отеля"""
        
        await self._check_and_get_hotel(self.db, hotel_id)
        await self._check_and_get_room(self.db, room_id)

        await self.db.rooms.delete(hotel_id=hotel_id, id=room_id)
        await self.db.commit()
        return {"status": "ok"}
