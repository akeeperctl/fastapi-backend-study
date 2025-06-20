from fastapi import APIRouter, HTTPException, Body
from fastapi.openapi.models import Example

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAddSchema, RoomPatchSchema, RoomAddRequestSchema, RoomPatchRequestSchema

router = APIRouter(prefix="/hotels", tags=["Комнаты отелей"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        db: DBDep,
        hotel_id: int
):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


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
        data: RoomAddRequestSchema = Body(openapi_examples={
            "1": Example(
                summary="Люкс комната",
                value={
                    "title": "Люкс комната",
                    "description": "Шикарная комната с телевизором и балконом",
                    "price": 10000,
                    "quantity": 4,
                }),

            "2": Example(
                summary="Обычная комната",
                value={
                    "title": "Обычная комната",
                    "description": "Обычная комната без балкона",
                    "price": 3000,
                    "quantity": 2,
                }),
        })
):
    _data = RoomAddSchema(hotel_id=hotel_id, **data.model_dump())
    rooms = await db.rooms.add(_data)
    await db.commit()
    return {"status": "ok", "data": rooms}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        data: RoomAddRequestSchema
):
    _data = RoomAddSchema(hotel_id=hotel_id, **data.model_dump())
    await db.rooms.edit(data=_data, id=room_id, hotel_id=hotel_id)
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
