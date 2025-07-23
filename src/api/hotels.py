from datetime import date
from typing import Optional

from fastapi import APIRouter, Body, HTTPException
from fastapi.openapi.models import Example
from fastapi.params import Query
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import (DateFromLaterDateToException, HotelNotFoundHTTPException,
                            HotelNotFoundException)
from src.schemas.hotels import HotelPatchSchema, HotelAddSchema
from src.services.hotels import HotelService

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
    try:
        hotels = await HotelService(db).get_hotels(
            pagination,
            title,
            location,
            date_from,
            date_to
        )
    except DateFromLaterDateToException as e:
        raise HTTPException(status_code=422, detail=e.detail)

    return {"status": "ok", "data": hotels}


@router.get("/{hotel_id}")
async def get_hotel(
        db: DBDep,
        hotel_id: int,
):
    try:
        hotel = await HotelService(db).get_hotel(hotel_id)
    except HotelNotFoundException:
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
    hotel = await HotelService(db).add_hotel(data)
    return {"status": "ok", "data": hotel}


# put передает ВСЕ параметры сущности, кроме ID. Создан для комплексного редактирования всей сущности
# patch передает какой-то один или несколько параметров. Создан для редактирования 1-2 параметров
@router.put("/{hotel_id}")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAddSchema):
    try:
        await HotelService(db).edit_hotel(hotel_id, hotel_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "ok"}


@router.patch("/{hotel_id}")
async def patch_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPatchSchema,
):
    try:
        await HotelService(db).patch_hotel(hotel_id, hotel_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "ok"}


# Чаще всего нужно делать так, чтобы удалялась конкретная сущность
@router.delete("/{hotel_id}")
async def delete_hotel(
        db: DBDep,
        hotel_id: int,
):
    try:
        await HotelService(db).delete_hotel(hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "ok"}
