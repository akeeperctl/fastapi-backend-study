from src.schemas.bookings import BookingAddRequestSchema, BookingAddSchema
from src.services.base import BaseService
from src.services.utils import DataChecker


class BookingService(BaseService, DataChecker):
    async def create_booking(
            self,
            user_id: int,
            booking_data: BookingAddRequestSchema,
    ):
        room = await self._check_and_get_room(self.db, booking_data.room_id)

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
        return await self.db.bookings.get_all()

    async def get_me_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)
