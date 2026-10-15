
from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import UploadFile
from sqlalchemy.orm import Session

from config.settings import get_settings
from exceptions.transport_collection_exception import (
    BadRequestException,
    NotFoundException,
)
from models.totals import CollectionTotals
from repositories.transport_collections_repository import (
    CollectionRepository,
)
from schemas.transport_collection_schema import CollectionResponse


ALLOWED_REPORT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "application/pdf": ".pdf",
}

MAX_REPORT_SIZE = 10 * 1024 * 1024


class CollectionService:
    def __init__(self, db: Session):
        self.repository = CollectionRepository(db)

    def calculate_totals(self,data: dict) -> CollectionTotals:
        total_trips = (data["morning_trips"] + data["evening_trips"])
        total_collection = (data["morning_collection"] + data["evening_collection"])
        total_expense = (data["fuel_expense"] + data["other_expense"])

        return CollectionTotals(
            total_trips=total_trips,
            total_collection=total_collection,
            total_expense=total_expense,
            net_collection=total_collection - total_expense,
        )

    def create(self, data: dict):
        totals = self.calculate_totals(data)

        values = {
            **data,
            "total_trips": totals.total_trips,
            "total_collection": totals.total_collection,
            "total_expense": totals.total_expense,
            "net_collection": totals.net_collection,
        }

        return self.repository.create(values)

    def get_by_id(self, collection_id: int):
        collection = self.repository.get_by_id(collection_id)

        if collection is None:
            raise NotFoundException("Collection id not found")

        return collection

    def get_all(self, page: int = 1, limit: int = 3):
        offset = (page - 1) * limit

        collections = self.repository.get_all(limit, offset)
        total_records = self.repository.get_total_count()

        total_pages = ((total_records + limit - 1) // limit)


        return {
            "items": [
                CollectionResponse.model_validate(item).model_dump(mode="json")
                for item in collections
            ],
            "total": total_pages,
            "page": page,
            "limit": limit,
        }

    def update(self, collection_id: int, changes: dict):
        collection = self.get_by_id(collection_id)

        required_fields = {
            "driver_name",
            "vehicle_number",
            "collection_date",
            "morning_trips",
            "evening_trips",
            "morning_collection",
            "evening_collection",
            "fuel_expense",
            "other_expense",
        }

        for field, value in changes.items():
            if value is None and field in required_fields:
                raise BadRequestException(
                    f"{field} cannot be null"
                )

        # Merge existing values with the incoming PATCH fields.
        data = {
            "morning_trips": collection.morning_trips,
            "evening_trips": collection.evening_trips,
            "morning_collection": collection.morning_collection,
            "evening_collection": collection.evening_collection,
            "fuel_expense": collection.fuel_expense,
            "other_expense": collection.other_expense,
        }

        data.update(changes)

        # Recalculate totals using the complete updated data.
        totals = self.calculate_totals(data)
        changes.update({
            "total_trips": totals.total_trips,
            "total_collection": totals.total_collection,
            "total_expense": totals.total_expense,
            "net_collection": totals.net_collection,
        })
        return self.repository.update(collection, changes)

    def delete(self, collection_id: int):
        collection = self.get_by_id(collection_id)
        self.repository.delete(collection)
        return {"message": "Collection deleted successfully"}

    
    def put(self, collection_id: int, data: dict):
        collection = self.get_by_id(collection_id)
        totals = self.calculate_totals(data)
        values = {
            **data,
            "total_trips": totals.total_trips,
            "total_collection": totals.total_collection,
            "total_expense": totals.total_expense,
            "net_collection": totals.net_collection,
        }
        return self.repository.update(collection, values)


    async def save_upload_file(self,file: UploadFile,collection_id: int) -> str:
        extension = ALLOWED_REPORT_TYPES.get(file.content_type)

        if extension is None:
            raise BadRequestException("Upload a JPG, PNG or PDF report")

        settings = get_settings()

        upload_folder = ( Path(settings.UPLOAD_FOLDER) / str(collection_id))
        upload_folder.mkdir(parents=True, exist_ok=True)

        file_path = upload_folder / f"{uuid4().hex}{extension}"
        total_size = 0

        try:
            async with aiofiles.open(file_path, "wb") as output:
                while True:
                    chunk = await file.read(1024 * 1024)
                    if not chunk:
                        break
                    total_size += len(chunk)
                    if total_size > MAX_REPORT_SIZE:
                        raise BadRequestException("Report file cannot exceed 10 MB")
                    await output.write(chunk)

        except Exception:
            file_path.unlink(missing_ok=True)
            raise

        finally:
            await file.close()

        return file_path.as_posix()

    async def upload_report(self,collection_id: int,file: UploadFile ):
        collection = self.get_by_id(collection_id)
        file_path = await self.save_upload_file(file,collection_id)
        
        try:
            self.repository.update_report(collection, file_path)
        except Exception:
            Path(file_path).unlink(missing_ok=True)
            raise

        return {
            "message": "Report uploaded successfully",
            "file_path": file_path,
        }
