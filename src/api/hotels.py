from typing import Optional

from fastapi import APIRouter, Body, HTTPException
from fastapi.openapi.models import Example
from fastapi.params import Query

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelPatchSchema, HotelAddSchema

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
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=page
        )


@router.get("/{id}")
async def get_hotel(id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Отель не найден")
        return {"status": "ok", "data": hotel}


# Чаще всего нужно делать так, чтобы удалялась конкретная сущность
@router.delete("/{id}")
async def delete_hotel(id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=id)
        await session.commit()

    return {"status": "ok"}


# request body
# title
@router.post("")
async def create_hotel(data: HotelAddSchema = Body(openapi_examples={
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
        hotel = await HotelsRepository(session).add(data)
        await session.commit()
        return {"status": "ok", "data": hotel}


# put передает ВСЕ параметры сущности, кроме ID. Создан для комплексного редактирования всей сущности
# patch передает какой-то один или несколько параметров. Создан для редактирования 1-2 параметров
@router.put("/{id}")
async def edit_hotel(id: int, data: HotelAddSchema):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data, id=id)
        await session.commit()

    return {"status": "ok"}


@router.patch("/{id}")
async def patch_hotel(id: int, data: HotelPatchSchema):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data, exclude_unset=True, id=id)
        await session.commit()

    return {"status": "ok"}
