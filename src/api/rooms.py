from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi.openapi.models import Example

from src.api.dependencies import DBDep
from src.exceptions import (
    RoomNotFoundHTTPException,
    HotelNotFoundHTTPException,
    RoomNotFoundException,
    HotelNotFoundException,
    DateFromLaterDateToException,
    DateFromLaterDateToHTTPException, InvalidFacilityIdException, InvalidFacilityIdHTTPException,
)
from src.schemas.rooms import (
    RoomAddRequestSchema,
    RoomPatchRequestSchema,
)
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Комнаты отелей"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(examples=["2025-07-01"]),
    date_to: date = Query(examples=["2025-07-07"]),
):
    try:
        rooms = await RoomService(db).get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
    except DateFromLaterDateToException as e:
        raise DateFromLaterDateToHTTPException from e

    return {"status": "ok", "data": rooms}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        room = await RoomService(db).get_room(room_id=room_id, hotel_id=hotel_id)
    except RoomNotFoundException as e:
        raise RoomNotFoundHTTPException from e

    return {"status": "ok", "data": room}


@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequestSchema = Body(
        openapi_examples={
            "1": Example(
                summary="Люкс номер",
                value={
                    "title": "Люкс номер",
                    "description": "Шикарный номер с телевизором и балконом",
                    "price": 10000,
                    "quantity": 2,
                    "facilities_ids": [],
                },
            ),
            "2": Example(
                summary="Обычный номер",
                value={
                    "title": "Обычный номер",
                    "description": "Обычный номер",
                    "price": 1000,
                    "quantity": 5,
                    "facilities_ids": [],
                },
            ),
        }
    ),
):
    try:
        room = await RoomService(db).create_room(hotel_id=hotel_id, room_data=room_data)
        if not room:
            raise RoomNotFoundHTTPException
    except HotelNotFoundException as e:
        raise HotelNotFoundHTTPException from e

    return {"status": "ok", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequestSchema):
    try:
        await RoomService(db).edit_room(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    except InvalidFacilityIdException as e:
        raise InvalidFacilityIdHTTPException from e
    except RoomNotFoundException as e:
        raise RoomNotFoundHTTPException from e
    except HotelNotFoundException as e:
        raise HotelNotFoundHTTPException from e

    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequestSchema):
    try:
        await RoomService(db).patch_room(hotel_id=hotel_id, room_id=room_id, room_data=room_data)
    except InvalidFacilityIdException as e:
        raise InvalidFacilityIdHTTPException from e
    except RoomNotFoundException as e:
        raise RoomNotFoundHTTPException from e
    except HotelNotFoundException as e:
        raise HotelNotFoundHTTPException from e

    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await RoomService(db).delete_room(hotel_id=hotel_id, room_id=room_id)
    except RoomNotFoundException as e:
        raise RoomNotFoundHTTPException from e
    except HotelNotFoundException as e:
        raise HotelNotFoundHTTPException from e

    await db.commit()
    return {"status": "ok"}
