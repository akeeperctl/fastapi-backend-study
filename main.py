import uvicorn
from fastapi import FastAPI

from hotels import router as hotels_router

app = FastAPI()

app.include_router(hotels_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":  # -> используется на проде
    uvicorn.run("main:app")
