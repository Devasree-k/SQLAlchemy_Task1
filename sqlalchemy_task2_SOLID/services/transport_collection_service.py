from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.transport_collection_model import TransportCollection
from repositories.transport_collection_repository import (
    TransportCollectionRepository,
)

from interfaces.transport_collection_repository_interface import TransportCollectionRepositoryInterface

class TransportCollectionService:

    def __init__(self, db: Session, collection_repository :TransportCollectionRepositoryInterface):
        self.db = db
        self.repository = collection_repository

    def calculate_totals(self, data: dict) -> dict:
        total_trips = (
            data["morning_trips"] + data["evening_trips"]
        )

        total_collection = (
            data["morning_collection"] + data["evening_collection"]
        )

        total_expense = (
            data["fuel_expense"] + data["other_expense"]
        )

        return {
            "total_trips": total_trips,
            "total_collection": total_collection,
            "total_expense": total_expense,
            "net_collection": total_collection - total_expense,
        }

    def get_collection(self, collection_id: int):
        collection = self.repository.get_by_id(collection_id)

        if collection is None:
            raise HTTPException(
                status_code=404,
                detail="Collection not found",
            )

        return collection

    def create_collection(self, data):
        values = data.model_dump()

        driver = self.repository.get_driver(
            values["driver_id"]
        )

        if driver is None:
            raise HTTPException(
                status_code=404,
                detail="Driver not found",
            )

        values.update(self.calculate_totals(values))

        collection = TransportCollection(**values)

        try:
            self.repository.create(collection)
            self.db.commit()

            return self.get_collection(collection.id)

        except Exception:
            self.db.rollback()
            raise

    def get_collections(self):
        return self.repository.get_all()

    def update_collection(
        self,
        collection_id: int,
        changes: dict,
    ):
        collection = self.get_collection(collection_id)

        values = {
            "driver_id": collection.driver_id,
            "vehicle_number": collection.vehicle_number,
            "collection_date": collection.collection_date,
            "morning_trips": collection.morning_trips,
            "evening_trips": collection.evening_trips,
            "morning_collection": collection.morning_collection,
            "evening_collection": collection.evening_collection,
            "fuel_expense": collection.fuel_expense,
            "other_expense": collection.other_expense,
        }

        values.update(changes)

        driver = self.repository.get_driver(
            values["driver_id"]
        )

        if driver is None:
            raise HTTPException(
                status_code=404,
                detail="Driver not found",
            )

        calculated = self.calculate_totals(values)

        try:
            for field, value in changes.items():
                setattr(collection, field, value)

            for field, value in calculated.items():
                setattr(collection, field, value)

            self.db.commit()

            return self.get_collection(collection_id)

        except Exception:
            self.db.rollback()
            raise

    def delete_collection(self, collection_id: int):
        collection = self.get_collection(collection_id)

        try:
            self.repository.delete(collection)
            self.db.commit()

            return {"message": "Collection deleted"}

        except Exception:
            self.db.rollback()
            raise
