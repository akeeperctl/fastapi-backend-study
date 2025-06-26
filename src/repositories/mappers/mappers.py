from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm

from src.schemas.bookings import BookingSchema
from src.schemas.facilities import FacilitySchema, RoomFacilitySchema
from src.schemas.hotels import HotelSchema
from src.schemas.rooms import RoomSchema
from src.schemas.users import UserSchema

from src.repositories.mappers.base import DataMapper


class BookingDataMapper(DataMapper):
    orm = BookingsOrm
    schema = BookingSchema


class FacilityDataMapper(DataMapper):
    orm = FacilitiesOrm
    schema = FacilitySchema


class RoomsFacilityDataMapper(DataMapper):
    orm = RoomsFacilitiesOrm
    schema = RoomFacilitySchema


class HotelDataMapper(DataMapper):
    orm = HotelsOrm
    schema = HotelSchema


class RoomDataMapper(DataMapper):
    orm = RoomsOrm
    schema = RoomSchema


class UserDataMapper(DataMapper):
    orm = UsersOrm
    schema = UserSchema
