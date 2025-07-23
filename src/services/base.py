from typing import Optional

from src.utils.db_manager import DBManager


class BaseService:
    db: Optional[DBManager]

    def __init__(self, db: Optional[DBManager] = None) -> None:
        self.db = db
