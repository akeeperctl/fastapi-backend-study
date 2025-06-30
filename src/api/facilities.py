import json

from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.init import redis_connector
from src.schemas.facilities import FacilityAddSchema

router = APIRouter(prefix="/facilities", tags=["Удобства в номере"])


@router.get("", description="Получить список всех возможных удобств")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return {"data": await db.facilities.get_all()}


@router.post("", description="Создать удобство")
async def create_facility(
        db: DBDep,
        facility_data: FacilityAddSchema = Body(),
):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "ok", "data": facility}
