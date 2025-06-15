from typing import Optional

import uvicorn
from fastapi import FastAPI
# from fastapi.openapi.docs import (
#     get_redoc_html,
#     get_swagger_ui_html,
#     get_swagger_ui_oauth2_redirect_html,
# )
from fastapi.params import Query

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
    {"id": 1, "title": "Дубай"},
    {"id": 2, "title": "Сочи"},
]


# Query параметры используются для фильтрации, сортировки (по близости, по рейтингу), пагинации
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


@app.get("/")
async def root():
    return {"message": " sddHello World!!!!!!"
                       "!!!!!!!"}


if __name__ == "__main__":  # -> используется на проде
    uvicorn.run("main:app", reload=True)
