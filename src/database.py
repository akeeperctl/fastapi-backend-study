from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

engine = create_async_engine(settings.DB_URL)

# bind-связать с движком
# expire_on_commit - ?
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


# нужен для того, чтобы мы наследовали все модели в проекте
class Base(DeclarativeBase):
    pass
