from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.bookings import BookingsRepository
from src.repositories.facilities import FacilitiesRepository, RoomsFacilitiesRepository
from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.repositories.users import UsersRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()

        self.hotels = HotelsRepository(session=self.session)
        self.rooms = RoomsRepository(session=self.session)
        self.users = UsersRepository(session=self.session)
        self.bookings = BookingsRepository(session=self.session)
        self.facilities = FacilitiesRepository(session=self.session)
        self.rooms_facilities = RoomsFacilitiesRepository(session=self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
