from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class HotelsOrm(Base):
    # название таблицы
    __tablename__ = 'hotels'

    # Если у нас нет специфических ограничений, то мы можем не использовать mapped_column()

    # primary_key=True делает столбец первичный ключ (он уникальный по определению, т.е. нет смысла в unique=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=100))
    location: Mapped[str]
