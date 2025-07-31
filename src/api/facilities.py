from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import (
    FacilityAlreadyExistsException,
    FacilityAlreadyExistsHTTPException,
    FacilityNotFoundException,
    FacilityNotFoundHTTPException,
)
from src.pydantic_types import EntityId
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
    try:
        facility = await FacilityService(db).add_facility(facility_data)
    except FacilityAlreadyExistsException as e:
        raise FacilityAlreadyExistsHTTPException from e
    return {"status": "ok", "data": facility}


@router.delete("/{facility_id}", description="Удалить удобство")
async def delete_facility(
    db: DBDep,
    facility_id: EntityId,
):
    try:
        await FacilityService(db).delete_facility(facility_id)
    except FacilityNotFoundException as e:
        raise FacilityNotFoundHTTPException from e
    return {"status": "ok"}
