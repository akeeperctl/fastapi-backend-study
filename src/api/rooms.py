from fastapi import APIRouter, HTTPException, Body
from fastapi.openapi.models import Example

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomsAddSchema, RoomsPatchSchema

router = APIRouter(prefix="/hotels", tags=["Комнаты отелей"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Комната отеля не найдена")
        return room


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, data: RoomsAddSchema = Body(openapi_examples={
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
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add_by_hotel_id(hotel_id, data)
        await session.commit()
        return {"status": "ok", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
        hotel_id: int,
        room_id: int,
        data: RoomsAddSchema
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=data, hotel_id=hotel_id, id=room_id)
        await session.commit()

        return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_room(
        hotel_id: int,
        room_id: int,
        data: RoomsPatchSchema
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
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
