from typing import Optional

from src.utils.db_manager import DBManager


class BaseService:
    """Базовый сервис, используется для создания новых сервисов приложения через наследование"""

    db: Optional[DBManager]

    def __init__(self, db: Optional[DBManager] = None) -> None:
        self.db = db
