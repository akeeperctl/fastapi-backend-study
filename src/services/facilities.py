from src.schemas.facilities import FacilityAddSchema
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def add_facility(self, facility_data: FacilityAddSchema):
        """Добавить удобство"""

        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()

        test_task.delay()
        return facility

    async def get_all(self):
        """Вернуть список всех удобств"""

        return await self.db.facilities.get_all()
