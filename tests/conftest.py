import json
import os

import pytest

from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAddSchema
from src.schemas.rooms import RoomAddSchema
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def is_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope='session', autouse=True)
async def setup_db_tables(is_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json") as f:
        hotels_data = json.load(f)
    with open("tests/mock_rooms.json") as f:
        rooms_data = json.load(f)

    _hotels = [HotelAddSchema.model_validate(hotel) for hotel in hotels_data]
    _rooms = [RoomAddSchema.model_validate(room) for room in rooms_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(_hotels)
        await db.rooms.add_bulk(_rooms)


@pytest.fixture(scope='session', autouse=True)
async def register_user(setup_db_tables):
    ts = ASGITransport(app=app)
    async with AsyncClient(transport=ts, base_url="http://localhost:8000/") as client:
        await client.post(
            "/auth/register",
            json={
                "email": "kot@pes.com",
                "password": "12345",
            }
        )
