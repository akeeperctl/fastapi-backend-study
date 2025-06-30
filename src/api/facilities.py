import json

from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.init import redis_connector
from src.schemas.facilities import FacilityAddSchema

router = APIRouter(prefix="/facilities", tags=["Удобства в номере"])


@router.get("", description="Получить список всех возможных удобств")
async def get_facilities(db: DBDep):
    facilities_from_cache = await redis_connector.get("facilities")
    if not facilities_from_cache:
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [fac.model_dump() for fac in facilities]
        facilities_json = json.dumps(facilities_schemas, indent=2, ensure_ascii=False)
        await redis_connector.set("facilities", facilities_json, expire=10)

        return {"data": facilities}
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return {"data": facilities_dicts}


@router.post("", description="Создать удобство")
async def create_facility(
        db: DBDep,
        facility_data: FacilityAddSchema = Body(),
):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "ok", "data": facility}
