from fastapi import APIRouter, HTTPException, Body
from fastapi.openapi.models import Example

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAddSchema, RoomPatchSchema, RoomAddRequestSchema, RoomPatchRequestSchema

router = APIRouter(prefix="/hotels", tags=["Комнаты отелей"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Комната отеля не найдена")
        return {"status": "ok", "data": room}


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, data: RoomAddRequestSchema = Body(openapi_examples={
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
})):
    _data = RoomAddSchema(hotel_id=hotel_id, **data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_data)
        await session.commit()
        return {"status": "ok", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
        hotel_id: int,
        room_id: int,
        data: RoomAddRequestSchema
):
    _data = RoomAddSchema(hotel_id=hotel_id, **data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=_data, id=room_id, hotel_id=hotel_id)
        await session.commit()

        return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
        hotel_id: int,
        room_id: int,
        data: RoomPatchRequestSchema
):
    # exclude_unset=True отбрасывает неуказанные свойства для изменения
    _data = RoomPatchSchema(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
        await session.commit()

        return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        hotel_id: int,
        room_id: int
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
        return {"status": "ok"}
