
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from exceptions.transport_collection_exception import (
    NotFoundException,
    ConflictException,
    BadRequestException,
)
from repositories.drivers_repository import DriverRepository

class DriverService:
    def __init__(self, db: Session):
        self.repo = DriverRepository(db)

    def create(self, data: dict):
        try:
            return self.repo.create(data)
        except IntegrityError as exc:
            raise ConflictException(
                "Phone or license number already exists"
            ) from exc

    def get(self, driver_id: int):
        driver = self.repo.get_by_id(driver_id)
        if driver is None:
            raise NotFoundException("Driver not found")
        return driver

    def list(self, page: int = 1, limit: int = 10):
        count = self.repo.count()
        items = self.repo.get_all(limit, (page - 1) * limit)
        return {
            "items": items,
            "total": count,
            "pages": (count + limit - 1) // limit,
            "page": page,
            "limit": limit,
        }

    def update(self, driver_id: int, changes: dict):
        driver = self.get(driver_id)
        if not changes:
            raise BadRequestException("Provide at least one field")
        try:
            return self.repo.update(driver, changes)
        except IntegrityError as exc:
            raise ConflictException(
                "Phone or license number already exists"
            ) from exc

    def delete(self, driver_id: int):
        driver = self.get(driver_id)

        if driver.collections:
            raise ConflictException(
                "Cannot delete a driver with collection records"
            )

        self.repo.delete(driver)
        return {"message": "Driver deleted successfully"}
