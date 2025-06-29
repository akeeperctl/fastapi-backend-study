from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

# исправление для того чтобы интерпретатор мог находить src
import sys
from pathlib import Path

from src.init import redis_connector

sys.path.append(str(Path(__file__).parent.parent))

from src.api.facilities import router as facilities_router
from src.api.bookings import router as bookings_router
from src.api.rooms import router as rooms_router
from src.api.hotels import router as hotels_router
from src.api.auth import router as auth_router
from src.config import settings
from src.database import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте проекта
    await redis_connector.connect()
    yield
    # При выключении/перезагрузки приложения
    await redis_connector.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":  # -> используется на проде
    uvicorn.run("main:app")
