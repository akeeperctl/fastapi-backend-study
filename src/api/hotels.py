import re
from typing import Optional

from fastapi import APIRouter, Body
from fastapi.openapi.models import Example
from fastapi.params import Query
from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import HotelSchema, HotelPatchSchema

# prefix - это путь к ручкам этого роутера
# tags - это категория в OpenAPI
router = APIRouter(prefix="/hotels", tags=["Отели"])


# Query параметры используются для фильтрации, сортировки (по близости, по рейтингу), пагинации
# Браузер в адресной строке всегда делает GET запрос
# gt - greater_then
# lt - lesser then
@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: Optional[str] = Query(default=None, description="Название отеля"),
        location: Optional[str] = Query(default=None, description="Местонахождение отеля")
):
    per_page = pagination.per_page or 5
    page = per_page * (pagination.page - 1)

    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if title:
            query = query.where(HotelsOrm.title.icontains(title.strip()))
        if location:
            query = query.where(HotelsOrm.location.icontains(location.strip()))

        query = (
            query
            .offset(page)
            .limit(per_page)
        )

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await session.execute(query)
        # result - итератор
        hotels = result.scalars().all()
        print(type(hotels), hotels)

        return hotels

    # start = (pagination.page - 1) * pagination.per_page
    # end = pagination.page * pagination.per_page


# Чаще всего нужно делать так, чтобы удалялась конкретная сущность
@router.delete("/{id}")
def delete_hotel(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != id]

    return {"status": "ok"}


# request body
# title
@router.post("")
async def create_hotel(hotel_data: HotelPatchSchema = Body(openapi_examples={
    "1": Example(
        summary="Сочи",
        value={
            "title": "Отель 5 звезд у моря",
            "location": "Сочи",
        }),

    "2": Example(
        summary="Дубай",
        value={
            "title": "Отель 5 звезд у песка",
            "location": "Дубай",
        }),
})):
    # Зачем нужен контекстный менеджер?
    # В Базе данных максимум 100 одновременных подключений.
    # Это может быть 100 разных пользователей, это может быть 1 алхимия, которая захватила 100 подключений
    # Каждый раз когда мы объявляем сессию мы захватываем/блокируем 5 подключений к базе данных.
    # Изначально Алхимия создает 5 подключений к БД. И лишь в случае большой нагрузки создает доп. 10 подключений.
    # Если не будем закрывать подключения и у нас будет 15 запросов, то 16 ый уже не пройдет.
    # Он упадет с ошибкой или в вечном ожидании.
    # Под сессией имеется ввиду какое-то подключение к базе данных.
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "ok"}


# put передает ВСЕ параметры сущности, кроме ID. Создан для комплексного редактирования всей сущности
# patch передает какой-то один или несколько параметров. Создан для редактирования 1-2 параметров
@router.put("/{id}")
def update_hotel(id: int, hotel_data: HotelSchema):
    global hotels
    ids = [hotel['id'] for hotel in hotels]
    if id not in ids:
        return {"status": "hotel not found"}

    hotel = hotels[ids.index(id)]
    hotel['title'] = hotel_data.title
    hotel['name'] = hotel_data.name

    return {"status": "ok"}


@router.patch("/{id}")
def patch_hotel(id: int, hotel_data: HotelPatchSchema):
    global hotels
    ids = [hotel['id'] for hotel in hotels]
    if id not in ids:
        return {"status": "hotel not found"}

    hotel = hotels[ids.index(id)]
    hotel['title'] = hotel_data.title if hotel_data.title and hotel_data.title != "string" else hotel['title']
    hotel['name'] = hotel_data.name if hotel_data.name and hotel_data.name != "string" else hotel['name']

    return {"status": "ok"}
