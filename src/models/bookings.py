from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from src.database import Base
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm


class BookingsOrm(Base):

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey(RoomsOrm.id))
    user_id: Mapped[int] = mapped_column(ForeignKey(UsersOrm.id))
    date_from: Mapped[datetime]
    date_to: Mapped[datetime]
    price: Mapped[int]
