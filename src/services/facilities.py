from src.schemas.facilities import FacilityAddSchema
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def create_facility(self, facility_data: FacilityAddSchema):
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()

        test_task.delay()
        return facility

    async def get_all(self):
        return await self.db.facilities.get_all()
