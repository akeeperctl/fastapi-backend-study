from src.config import settings
from src.connectors.redis_connector import RedisConnector

redis_connector = RedisConnector(settings.REDIS_HOST, settings.REDIS_PORT)
