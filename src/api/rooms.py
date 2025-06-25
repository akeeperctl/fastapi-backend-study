from datetime import date

from fastapi import APIRouter, HTTPException, Body, Query
from fastapi.openapi.models import Example

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAddSchema
from src.schemas.rooms import RoomAddSchema, RoomPatchSchema, RoomAddRequestSchema, RoomPatchRequestSchema

router = APIRouter(prefix="/hotels", tags=["Комнаты отелей"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2025-07-01"),
        date_to: date = Query(example="2025-07-07"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    room = await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Комната отеля не найдена")
    return {"status": "ok", "data": room}


@router.post("/{hotel_id}/rooms")
async def create_room(
        db: DBDep,
        hotel_id: int,
        room_data: RoomAddRequestSchema = Body(openapi_examples={
            "1": Example(
                summary="Люкс номер",
                value={
                    "title": "Люкс номер",
                    "description": "Шикарный номер с телевизором и балконом",
                    "price": 10000,
                    "quantity": 2,
                    "facilities_ids": []
                }),

            "2": Example(
                summary="Обычный номер",
                value={
                    "title": "Обычный номер",
                    "description": "Обычный номер",
                    "price": 1000,
                    "quantity": 5,
                    "facilities_ids": []
                }),
        })
):
    _room_data = RoomAddSchema(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    room_facilities_data = [
        RoomFacilityAddSchema(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(room_facilities_data)

    await db.commit()
    return {"status": "ok", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        data: RoomAddRequestSchema
):
    _data = RoomAddSchema(hotel_id=hotel_id, **data.model_dump())
    await db.rooms.edit(data=_data, id=room_id, hotel_id=hotel_id)
    await db.rooms_facilities.replace_facilities(room_id=room_id, facilities_ids=data.facilities_ids)
    await db.commit()
    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        data: RoomPatchRequestSchema
):
    # exclude_unset=True отбрасывает неуказанные свойства для изменения
    _data = RoomPatchSchema(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))
    await db.rooms.edit(data=_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
    await db.rooms_facilities.replace_facilities(room_id=room_id, facilities_ids=data.facilities_ids)
    await db.commit()
    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "ok"}
