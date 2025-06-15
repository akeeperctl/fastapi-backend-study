from typing import Optional

import uvicorn
from fastapi import FastAPI
# from fastapi.openapi.docs import (
#     get_redoc_html,
#     get_swagger_ui_html,
#     get_swagger_ui_oauth2_redirect_html,
# )
from fastapi.params import Query, Body

app = FastAPI()

# Исправление долгой загрузки /docs. Взято из документации.
# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         openapi_url=app.openapi_url,
#         title=app.title + " - Swagger UI",
#         oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
#         swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
#         swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
#     )


hotels = [
    {"id": 1, "title": "Дубай", "name": "dubai"},
    {"id": 2, "title": "Сочи", "name": "sochi"},
]


# Query параметры используются для фильтрации, сортировки (по близости, по рейтингу), пагинации
# Браузер в адресной строке всегда делает GET запрос
@app.get("/hotels")
def get_hotels(id: Optional[int] = Query(default=None, description="Идентификатор отеля"),
               title: Optional[str] = Query(default=None, description="Название отеля")):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue

        hotels_.append(hotel)

    return {"data": hotels_}


# Чаще всего нужно делать так, чтобы удалялась конкретная сущность
@app.delete("/hotels{id}")
def delete_hotel(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != id]

    return {"status": "ok"}


# request body
# title
@app.post("/hotels")
def create_hotel(title: str = Body(embed=True), name: str = Body(embed=True)):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
    })

    return {"status": "ok"}


# put передает ВСЕ параметры сущности, кроме ID. Создан для комплексного редактирования всей сущности
# patch передает какой-то один или несколько параметров. Создан для редактирования 1-2 параметров
@app.put("/hotels/{id}")
def update_hotel(id: int,
                 title: str = Body(embed=True),
                 name: str = Body(embed=True)):

    global hotels
    ids = [hotel['id'] for hotel in hotels]
    if id not in ids:
        return {"status": "hotel not found"}

    hotel = hotels[ids.index(id)]
    hotel['title'] = title
    hotel['name'] = name

    return {"status": "ok"}


@app.patch("/hotels/{id}")
def patch_hotel(id: int,
                title: Optional[str] = Body(default=None),
                name: Optional[str] = Body(default=None)):

    global hotels
    ids = [hotel['id'] for hotel in hotels]
    if id not in ids:
        return {"status": "hotel not found"}

    hotel = hotels[ids.index(id)]
    hotel['title'] = title if title else hotel['title']
    hotel['name'] = name if name else hotel['name']

    return {"status": "ok"}


@app.get("/")
async def root():
    return {"message": " sddHello World!!!!!!"
                       "!!!!!!!"}


if __name__ == "__main__":  # -> используется на проде
    uvicorn.run("main:app")
