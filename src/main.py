import uvicorn
from fastapi import FastAPI

# исправление для того чтобы интерпретатор мог находить src
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.api.auth import router as auth_router
from src.config import settings
from src.database import *

app = FastAPI()

app.include_router(auth_router)
app.include_router(hotels_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":  # -> используется на проде
    uvicorn.run("main:app")
