from typing import Optional

from fastapi import APIRouter
from fastapi.params import Query, Body

hotels = [
    {"id": 1, "title": "Дубай", "name": "dubai"},
    {"id": 2, "title": "Сочи", "name": "sochi"},
]

# prefix - это путь к ручкам этого роутера
# tags - это категория в OpenAPI
router = APIRouter(prefix="/hotels", tags=["Отели"])


# Query параметры используются для фильтрации, сортировки (по близости, по рейтингу), пагинации
# Браузер в адресной строке всегда делает GET запрос
@router.get("")
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
@router.delete("/{id}")
def delete_hotel(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != id]

    return {"status": "ok"}


# request body
# title
@router.post("")
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
@router.put("/{id}")
def update_hotel(id: int,
                 title: str = Body(),
                 name: str = Body()):
    global hotels
    ids = [hotel['id'] for hotel in hotels]
    if id not in ids:
        return {"status": "hotel not found"}

    hotel = hotels[ids.index(id)]
    hotel['title'] = title
    hotel['name'] = name

    return {"status": "ok"}


@router.patch("/{id}")
def patch_hotel(id: int,
                title: Optional[str] = Body(default=None),
                name: Optional[str] = Body(default=None)):
    global hotels
    ids = [hotel['id'] for hotel in hotels]
    if id not in ids:
        return {"status": "hotel not found"}

    hotel = hotels[ids.index(id)]
    hotel['title'] = title if title and title != "string" else hotel['title']
    hotel['name'] = name if name and name != "string" else hotel['name']

    return {"status": "ok"}
