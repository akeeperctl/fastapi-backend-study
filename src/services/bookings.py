from src.pydantic_types import EntityId
from src.schemas.bookings import BookingAddRequestSchema, BookingAddSchema
from src.services.base import BaseService
from src.services.utils import DataChecker


class BookingService(BaseService, DataChecker):
    async def add_booking(
        self,
        user_id: EntityId,
        booking_data: BookingAddRequestSchema,
    ):
        """Добавить бронирование номера указанному пользователю"""

        room = await self._check_and_get_room(self.db, booking_data.room_id)

        # TODO: дата заезда не может быть раньше чем сегодня. Т.е нельзя бронировать время заезда на вчера)
        self._check_dates(booking_data.date_from, booking_data.date_to)

        price_per_day = room.price
        days = max((booking_data.date_to - booking_data.date_from).days, 1)
        final_price = price_per_day * days

        _booking_data = BookingAddSchema(
            price=final_price, user_id=user_id, **booking_data.model_dump()
        )

        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
        await self.db.commit()

        return booking

    async def get_bookings(self):
        """Вернуть список всех бронирований"""

        return await self.db.bookings.get_all()

    async def get_me_bookings(self, user_id: int):
        """Вернуть список бронирований определенного пользователя"""

        return await self.db.bookings.get_filtered(user_id=user_id)
