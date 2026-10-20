
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from dependencies.database import get_database
from schemas.driver_schema import (
    DriverCreate, DriverUpdate, DriverResponse
)
from services.driver_service import DriverService

router = APIRouter(
    prefix="/api/v1/drivers",
    tags=["Drivers"],
)

@router.post("/", response_model=DriverResponse,
             status_code=status.HTTP_201_CREATED)
def create_driver(
    data: DriverCreate,
    db: Session = Depends(get_database),
):
    return DriverService(db).create(data.model_dump())

@router.get("/")
def list_drivers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_database),
):
    return DriverService(db).list(page, limit)

@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(
    driver_id: int,
    db: Session = Depends(get_database),
):
    return DriverService(db).get(driver_id)

@router.patch("/{driver_id}", response_model=DriverResponse)
def update_driver(
    driver_id: int,
    data: DriverUpdate,
    db: Session = Depends(get_database),
):
    return DriverService(db).update(
        driver_id, data.model_dump(exclude_unset=True)
    )

@router.delete("/{driver_id}")
def delete_driver(
    driver_id: int,
    db: Session = Depends(get_database),
):
    return DriverService(db).delete(driver_id)
