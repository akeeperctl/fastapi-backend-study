from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UsersOrm(Base):
    # название таблицы
    __tablename__ = 'users'

    # Если у нас нет специфических ограничений, то мы можем не использовать mapped_column()

    # primary_key=True делает столбец первичный ключ (он уникальный по определению, т.е. нет смысла в unique=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200))
    hashed_password: Mapped[str] = mapped_column(String(200))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    nick_name: Mapped[str] = mapped_column(String(100))

