# ruff: noqa: E402 F403

import json
from unittest import mock

import pytest
from httpx import AsyncClient, ASGITransport
from loguru import logger

from src.schemas.facilities import FacilityAddSchema
from src.schemas.users import UserRequestAddSchema
from src.schemas.hotels import HotelAddSchema
from src.schemas.rooms import RoomAddSchema
from src.utils.db_manager import DBManager
from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *

# mock patch'и должны быть определены до импорта того, что мокается
mock.patch("fastapi_cache.decorator.cache", new=lambda *args, **kwargs: lambda f: f).start()
from src.main import app


@pytest.fixture(scope="session", autouse=True)
async def is_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session")
async def ac():
    ts = ASGITransport(app=app)
    async with AsyncClient(transport=ts, base_url="http://localhost:8000/") as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
async def setup_database(is_test_mode):
    logger.info(f"Подключение к БД host={settings.DB_HOST} port={settings.DB_PORT}")
    try:
        async with engine_null_pool.begin() as conn:
            logger.info(f"Подключение к БД успешно! host={settings.DB_HOST} port={settings.DB_PORT}")
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

            settings.DB_AVAILABLE = True
    except Exception as e:
        logger.critical(f"Не удалось подключиться к БД. Тип ошибки: {type(e)}")
        settings.DB_AVAILABLE = False

    with open("tests/mock_hotels.json") as f:
        hotels_data = json.load(f)
    with open("tests/mock_rooms.json") as f:
        rooms_data = json.load(f)
    with open("tests/mock_facilities.json") as f:
        facilities_data = json.load(f)

    _hotels = [HotelAddSchema.model_validate(hotel) for hotel in hotels_data]
    _rooms = [RoomAddSchema.model_validate(room) for room in rooms_data]
    _facilities = [FacilityAddSchema.model_validate(facility) for facility in facilities_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as _db:
        await _db.facilities.add_bulk(_facilities)
        await _db.hotels.add_bulk(_hotels)
        await _db.rooms.add_bulk(_rooms)
        await _db.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    await ac.post(
        "/auth/register",
        json=UserRequestAddSchema(
            email="kot@pes.com",
            password="12345",
        ).model_dump(),
    )


@pytest.fixture(scope="session")
async def logged_in_ac(register_user, ac):
    await ac.post(
        "/auth/login",
        json=UserRequestAddSchema(
            email="kot@pes.com",
            password="12345",
        ).model_dump(),
    )

    assert ac.cookies["access_token"]

    yield ac
