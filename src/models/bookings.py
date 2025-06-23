from datetime import date, datetime

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

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

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )
