from datetime import date
from typing import Optional

from src.schemas.hotels import HotelAddSchema, HotelPatchSchema
from src.services.base import BaseService
from src.services.utils import DataChecker


class HotelService(BaseService, DataChecker):
    async def get_hotels(
        self,
        pagination,
        title: Optional[str],
        location: Optional[str],
        date_from: date,
        date_to: date,
    ):
        self._check_dates(date_from, date_to)
        per_page = pagination.per_page or 5
        page = per_page * (pagination.page - 1)

        hotels = await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=page,
        )

        return hotels

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, hotel_data: HotelAddSchema):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def edit_hotel(self, hotel_id: int, hotel_data: HotelAddSchema) -> None:
        await self._check_and_get_hotel(self.db, hotel_id)

        await self.db.hotels.edit(id=hotel_id, data=hotel_data)
        await self.db.commit()

    async def patch_hotel(self, hotel_id: int, hotel_data: HotelPatchSchema) -> None:
        await self._check_and_get_hotel(self.db, hotel_id)

        await self.db.hotels.edit(id=hotel_id, data=hotel_data, exclude_unset=True)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self._check_and_get_hotel(self.db, hotel_id)

        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
