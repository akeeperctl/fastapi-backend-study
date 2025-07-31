from src.exceptions import (ObjectAlreadyExistsException, FacilityAlreadyExistsException)
from src.schemas.facilities import FacilityAddSchema
from src.services.base import BaseService
from src.services.utils import DataChecker
from src.tasks.tasks import test_task


class FacilityService(BaseService, DataChecker):
    async def add_facility(self, facility_data: FacilityAddSchema):
        """Добавить удобство"""

        try:
            facility = await self.db.facilities.add(facility_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as e:
            raise FacilityAlreadyExistsException from e

        test_task.delay()
        return facility

    async def get_all(self):
        """Вернуть список всех удобств"""

        return await self.db.facilities.get_all()

    async def delete_facility(self, facility_id: int):
        await self._check_and_get_facility(self.db, facility_id)
        await self.db.facilities.delete(id=facility_id)
        await self.db.commit()
