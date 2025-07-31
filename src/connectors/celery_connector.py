from celery import Celery
from kombu.exceptions import OperationalError
from loguru import logger

from src.exceptions import CeleryBrokerNotAvailableException


class CeleryConnector:

    def __init__(self, broker: str, backend: str, include: list[str]):
        self.broker = broker
        self.backend = backend
        self.include = include
        self.celery = Celery(
            main="tasks",
            broker=self.broker,
            backend=self.backend,
            include=self.include
        )

        self.celery.conf.beat_schedule = {
            "luboe-nazvanie": {
                "task": "booking_today_checkin",
                "schedule": 5,  # sec or crotab syntax
            }
        }

    def connect(self):
        logger.info(f"Подключение Celery к брокеру broker={self.broker} backend={self.backend}")

        try:
            with self.celery.connection() as conn:
                conn.ensure_connection(max_retries=1)
                logger.info(f"Успешное подключение Celery к брокеру broker={self.broker} backend={self.backend}")
        except OperationalError as e:
            logger.error(f"Celery не удалось подключиться к брокеру broker={self.broker} backend={self.backend}")
            raise CeleryBrokerNotAvailableException from e

    async def close(self):
        if self.celery:
            self.celery.close()
