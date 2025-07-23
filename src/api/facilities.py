from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAddSchema
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства в номере"])


@router.get("", description="Получить список всех возможных удобств")
@cache(expire=10)
async def get_facilities(db: DBDep):
    facilities = await FacilityService(db).get_all()
    return {"status": "ok", "data": facilities}


@router.post("", description="Создать удобство")
async def create_facility(
    db: DBDep,
    facility_data: FacilityAddSchema = Body(),
):
    facility = await FacilityService(db).create_facility(facility_data)
    return {"status": "ok", "data": facility}
