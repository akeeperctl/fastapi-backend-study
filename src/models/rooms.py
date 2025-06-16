from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.models.hotels import HotelsOrm


class RoomsOrm(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey(HotelsOrm.id))
    title: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    quantity: Mapped[int]


