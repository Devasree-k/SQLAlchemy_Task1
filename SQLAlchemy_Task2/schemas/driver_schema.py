
from pydantic import BaseModel, ConfigDict, Field

class DriverCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=20)
    license_number: str = Field(min_length=1, max_length=50)

class DriverUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=20)
    license_number: str | None = Field(default=None, min_length=1, max_length=50)

class DriverResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str | None
    license_number: str
