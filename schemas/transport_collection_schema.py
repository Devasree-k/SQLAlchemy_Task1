from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class CollectionCreate(BaseModel):
    driver_name: str
    vehicle_number: str
    collection_date: date
    morning_trips: int
    evening_trips: int
    morning_collection: Decimal
    evening_collection: Decimal
    fuel_expense: Decimal
    other_expense: Decimal
    total_trips: int
    total_collection: Decimal
    total_expense: Decimal
    net_collection: Decimal
    report_file: str | None = None


class CollectionResponse(CollectionCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CollectionUpdate(BaseModel):
    driver_name: str | None = None
    vehicle_number: str | None = None
    collection_date: date | None = None
    morning_trips: int | None = None
    evening_trips: int | None = None
    morning_collection: Decimal | None = None
    evening_collection: Decimal | None = None
    fuel_expense: Decimal | None = None
    other_expense: Decimal | None = None
    total_trips: int | None = None
    total_collection: Decimal | None = None
    total_expense: Decimal | None = None
    net_collection: Decimal | None = None
    report_file: str | None = None
