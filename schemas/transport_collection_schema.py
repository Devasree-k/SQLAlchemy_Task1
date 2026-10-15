
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CollectionCreate(BaseModel):
    driver_name: str
    vehicle_number: str
    collection_date: date
    morning_trips: int = Field(ge=0)
    evening_trips: int = Field(ge=0)
    morning_collection: Decimal = Field(ge=0)
    evening_collection: Decimal = Field(ge=0)
    fuel_expense: Decimal = Field(ge=0)
    other_expense: Decimal = Field(ge=0)



class CollectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
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


class CollectionUpdate(BaseModel):
    driver_name: str | None = None
    vehicle_number: str | None = None
    collection_date: date | None = None
    morning_trips: int | None = Field(default=None, ge=0)
    evening_trips: int | None = Field(default=None, ge=0)
    morning_collection: Decimal | None = Field(default=None, ge=0)
    evening_collection: Decimal | None = Field(default=None, ge=0)
    fuel_expense: Decimal | None = Field(default=None, ge=0)
    other_expense: Decimal | None = Field(default=None, ge=0)
    report_file: str | None = None


class CollectionPut(BaseModel):

    driver_name: str
    vehicle_number: str
    collection_date: date
    morning_trips: int = Field(ge=0)
    evening_trips: int = Field(ge=0)
    morning_collection: Decimal = Field(ge=0)
    evening_collection: Decimal = Field(ge=0)
    fuel_expense: Decimal = Field(ge=0)
    other_expense: Decimal = Field(ge=0)

