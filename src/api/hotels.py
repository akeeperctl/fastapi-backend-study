from datetime import date
from typing import Optional

from fastapi import APIRouter, Body, HTTPException
from fastapi.openapi.models import Example
from fastapi.params import Query
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import (DateFromLaterThanDateToException, ObjectNotExistException, check_date_from_later_date_to,
                            HotelNotFoundHTTPException)
from src.schemas.hotels import HotelPatchSchema, HotelAddSchema

# prefix - это путь к ручкам этого роутера
# tags - это категория в OpenAPI
router = APIRouter(prefix="/hotels", tags=["Отели"])


# Query параметры используются для фильтрации, сортировки (по близости, по рейтингу), пагинации
# Браузер в адресной строке всегда делает GET запрос
# gt - greater_then
# lt - lesser then
@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: Optional[str] = Query(default=None, description="Название отеля"),
    location: Optional[str] = Query(default=None, description="Местонахождение отеля"),
    date_from: date = Query(examples=["2025-07-01"]),
    date_to: date = Query(examples=["2025-07-07"]),
):
    check_date_from_later_date_to(date_from, date_to)
    per_page = pagination.per_page or 5
    page = per_page * (pagination.page - 1)

    try:
        hotels = await db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=page,
        )
    except DateFromLaterThanDateToException as e:
        raise HTTPException(status_code=422, detail=e.detail)

    return hotels


@router.get("/{hotel_id}")
async def get_hotel(
    db: DBDep,
    hotel_id: int,
):
    try:
        hotel = await db.hotels.get_one(id=hotel_id)
    except ObjectNotExistException:
        raise HotelNotFoundHTTPException
    return {"status": "ok", "data": hotel}


# request body
# title
@router.post("")
async def create_hotel(
    db: DBDep,
    data: HotelAddSchema = Body(
        openapi_examples={
            "1": Example(
                summary="Сочи",
                value={
                    "title": "Отель 5 звезд у моря",
                    "location": "Сочи",
                },
            ),
            "2": Example(
                summary="Дубай",
                value={
                    "title": "Отель 5 звезд у песка",
                    "location": "Дубай",
                },
            ),
        }
    ),
):
    hotel = await db.hotels.add(data)
    await db.commit()
    return {"status": "ok", "data": hotel}


# put передает ВСЕ параметры сущности, кроме ID. Создан для комплексного редактирования всей сущности
# patch передает какой-то один или несколько параметров. Создан для редактирования 1-2 параметров
@router.put("/{hotel_id}")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAddSchema):
    await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.patch("/{hotel_id}")
async def patch_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPatchSchema,
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "ok"}


# Чаще всего нужно делать так, чтобы удалялась конкретная сущность
@router.delete("/{hotel_id}")
async def delete_hotel(
    db: DBDep,
    hotel_id: int,
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "ok"}
