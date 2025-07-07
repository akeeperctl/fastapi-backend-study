import json

import pytest

from httpx import AsyncClient, ASGITransport

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *
from src.main import app
from src.schemas.hotels import HotelAddSchema
from src.schemas.rooms import RoomAddSchema
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def is_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope='function')
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope='session')
async def ac():
    ts = ASGITransport(app=app)
    async with AsyncClient(transport=ts, base_url="http://localhost:8000/") as client:
        yield client


@pytest.fixture(scope='session', autouse=True)
async def setup_database(is_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json") as f:
        hotels_data = json.load(f)
    with open("tests/mock_rooms.json") as f:
        rooms_data = json.load(f)

    _hotels = [HotelAddSchema.model_validate(hotel) for hotel in hotels_data]
    _rooms = [RoomAddSchema.model_validate(room) for room in rooms_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as _db:
        await _db.hotels.add_bulk(_hotels)
        await _db.rooms.add_bulk(_rooms)
        await _db.commit()


@pytest.fixture(scope='session', autouse=True)
async def register_user(setup_database, ac):
    await ac.post(
        "/auth/register",
        json={
            "email": "kot@pes.com",
            "password": "12345",
        }
    )
