from pydantic import BaseModel, Field

class DriverCreate(BaseModel):
    driver_name: str = Field(min_length=2, max_length=100)
    phone_number: str = Field(pattern="^[6-9][0-9]{9}$")

class DriverResponse(BaseModel):
    driver_id: int
    driver_name: str
    phone_number: str
