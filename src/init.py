from src.config import settings
from src.connectors.celery_connector import CeleryConnector
from src.connectors.redis_connector import RedisConnector

redis_connector = RedisConnector(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT
)
celery_connector = CeleryConnector(
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["src.tasks.tasks"]
)
