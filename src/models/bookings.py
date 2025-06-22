from datetime import datetime, date

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from src.database import Base
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm


class BookingsOrm(Base):

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey(RoomsOrm.id, ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey(UsersOrm.id, ondelete="CASCADE"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]
