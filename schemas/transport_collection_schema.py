from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field

class CollectionCreate(BaseModel):
    driver_id: int = Field(gt=0)
    vehicle_number: str = Field(min_length=5, max_length=20)
    collection_date: date
    morning_trips: int = Field(ge=0)
    evening_trips: int = Field(ge=0)
    morning_collection: Decimal = Field(ge=0)
    evening_collection: Decimal = Field(ge=0)
    fuel_expense: Decimal = Field(ge=0)
    other_expense: Decimal = Field(ge=0)

class CollectionResponse(BaseModel):
    id: int
    driver_id: int
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


class CollectionPatch(BaseModel):
    driver_id: int | None = Field(default=None, gt=0)
    vehicle_number: str | None = Field(default=None, min_length=5, max_length=20)
    collection_date: date | None = None
    morning_trips: int | None = Field(default=None, ge=0)
    evening_trips: int | None = Field(default=None, ge=0)
    morning_collection: Decimal | None = Field(default=None, ge=0)
    evening_collection: Decimal | None = Field(default=None, ge=0)
    fuel_expense: Decimal | None = Field(default=None, ge=0)
    other_expense: Decimal | None = Field(default=None, ge=0)
