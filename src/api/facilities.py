from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAddSchema

router = APIRouter(prefix="/facilities", tags=["Удобства в номере"])


@router.get("", description="Получить список всех возможных удобств")
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
