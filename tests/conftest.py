import json
import os

import pytest

from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *


@pytest.fixture(scope="session", autouse=True)
async def is_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope='session', autouse=True)
async def setup_db_tables(is_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


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


@pytest.fixture(scope='session', autouse=True)
async def add_mock_hotels(setup_db_tables):
    ts = ASGITransport(app=app)
    async with AsyncClient(transport=ts, base_url="http://localhost:8000/") as client:
        with open("tests/mock_hotels.json") as f:
            data: list[dict] = json.load(f)

            for i in data:
                await client.post(
                    "/hotels",
                    json=i
                )


@pytest.fixture(scope='session', autouse=True)
async def add_mock_rooms(add_mock_hotels):
    ts = ASGITransport(app=app)
    async with AsyncClient(transport=ts, base_url="http://localhost:8000/") as client:
        with open("tests/mock_rooms.json") as f:
            data: list[dict] = json.load(f)

            for i in data:
                await client.post(
                    f"hotels/{i['hotel_id']}/rooms",
                    json=i
                )
