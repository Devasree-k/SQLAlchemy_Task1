
from pathlib import Path
from uuid import uuid4
from decimal import Decimal

import aiofiles
from fastapi import UploadFile
from sqlalchemy.orm import Session

from config.settings import get_settings
from exceptions.transport_collection_exception import (
    BadRequestException,
    NotFoundException,
)
from models.driver_model import Driver
from models.totals import CollectionTotals
from repositories.transport_collections_repository import CollectionRepository

ALLOWED_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "application/pdf": ".pdf",
}
MAX_FILE_SIZE = 10 * 1024 * 1024

class CollectionService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CollectionRepository(db)

    def calculate_totals(self, data: dict) -> CollectionTotals:
        total_trips = data["morning_trips"] + data["evening_trips"]
        total_collection = (
            data["morning_collection"] + data["evening_collection"]
        )
        total_expense = data["fuel_expense"] + data["other_expense"]

        return CollectionTotals(
            total_trips=total_trips,
            total_collection=total_collection,
            total_expense=total_expense,
            net_collection=total_collection - total_expense,
        )

    def prepare_data(self, data: dict) -> dict:
        values = dict(data)
        totals = self.calculate_totals(values)
        values.update({
            "total_trips": totals.total_trips,
            "total_collection": totals.total_collection,
            "total_expense": totals.total_expense,
            "net_collection": totals.net_collection,
        })
        return values

    def ensure_driver(self, driver_id: int):
        if self.db.get(Driver, driver_id) is None:
            raise BadRequestException(
                f"Driver {driver_id} does not exist"
            )

    def get_by_id(self, item_id: int):
        item = self.repo.get_by_id(item_id)
        if item is None:
            raise NotFoundException("Collection not found")
        return item

    def create(self, data: dict):
        self.ensure_driver(data["driver_id"])
        return self.repo.create(self.prepare_data(data))

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

    def update(self, item_id: int, changes: dict):
        item = self.get_by_id(item_id)

        # PATCH: update only supplied fields.
        required = (
            "driver_id", "vehicle_number", "collection_date",
            "morning_trips", "evening_trips", "morning_collection",
            "evening_collection", "fuel_expense", "other_expense",
        )

        for key in required:
            if key in changes and changes[key] is None:
                raise BadRequestException(f"{key} cannot be null")

        if not changes:
            raise BadRequestException("Provide at least one field")

        if "driver_id" in changes:
            self.ensure_driver(changes["driver_id"])

        values = {
            key: getattr(item, key)
            for key in (
                "morning_trips", "evening_trips",
                "morning_collection", "evening_collection",
                "fuel_expense", "other_expense",
            )
        }
        values.update({
            key: value for key, value in changes.items()
            if key in values
        })

        totals = self.calculate_totals(values)
        changes.update({
            "total_trips": totals.total_trips,
            "total_collection": totals.total_collection,
            "total_expense": totals.total_expense,
            "net_collection": totals.net_collection,
        })

        return self.repo.update(item, changes)

    # def replace(self, item_id: int, data: dict):
    #     self.get_by_id(item_id)
    #     self.ensure_driver(data["driver_id"])
    #     return self.repo.update(item_id=self.get_by_id(item_id), changes=self.prepare_data(data))


    
    def replace(self, item_id: int, data: dict):
        item = self.get_by_id(item_id)
        self.ensure_driver(data["driver_id"])
        return self.repo.update(item, self.prepare_data(data))



    def delete(self, item_id: int):
        item = self.get_by_id(item_id)
        self.repo.delete(item)
        return {"message": "Collection deleted successfully"}

    async def upload_report(self, item_id: int, file: UploadFile):
        item = self.get_by_id(item_id)
        extension = ALLOWED_TYPES.get(file.content_type)

        if not extension:
            raise BadRequestException(
                "Only JPG, PNG and PDF reports are allowed"
            )

        folder = Path(get_settings().UPLOAD_FOLDER) / str(item_id)
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{uuid4().hex}{extension}"
        size = 0

        try:
            async with aiofiles.open(path, "wb") as output:
                while True:
                    chunk = await file.read(1024 * 1024)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > MAX_FILE_SIZE:
                        raise BadRequestException(
                            "Report must be 10 MB or smaller"
                        )
                    await output.write(chunk)

            self.repo.update_report(item, str(path))
        except Exception:
            path.unlink(missing_ok=True)
            raise
        finally:
            await file.close()

        return {"message": "Report uploaded successfully",
                "file_path": str(path)}
