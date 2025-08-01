from loguru import logger
from sqlalchemy import MetaData, NullPool, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings
from src.exceptions import DBNotAvailableException

engine = create_async_engine(settings.DB_URL)
engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool)

# bind-связать с движком
# expire_on_commit - ?
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
async_session_maker_null_pool = async_sessionmaker(bind=engine_null_pool, expire_on_commit=False)


# нужен для того, чтобы мы наследовали все модели в проекте
class Base(DeclarativeBase):
    # нужно для того, чтобы алхимия генерировала имена ограничений,
    # которые алембик будет использовать для подстановки
    # иначе они будут None и алембик подставит None, что не даст сделать alembic downgrade,
    # т.к. alembic будет пытаться удалить ограничение, которое ищет по НЕУКАЗАННОМУ ИМЕНИ
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    pass


async def check_db_connection():
    logger.info(f"Подключение к БД host={settings.DB_HOST} port={settings.DB_PORT}")

    try:
        async with async_session_maker() as session:
            await session.execute(text("SELECT 1"))
            await session.commit()
            logger.info(
                f"Подключение к БД успешно! host={settings.DB_HOST} port={settings.DB_PORT}"
            )
    except Exception as e:
        logger.critical(f"Не удалось подключиться к БД. Тип ошибки: {type(e)}")
        raise DBNotAvailableException from e
