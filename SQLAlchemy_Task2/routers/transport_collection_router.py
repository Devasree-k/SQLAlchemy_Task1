
from fastapi import (
    APIRouter, Depends, File, Query, UploadFile, status
)
from sqlalchemy.orm import Session

from dependencies.database import get_database
from schemas.transport_collection_schema import (
    CollectionCreate, CollectionPut, CollectionUpdate,
    CollectionResponse,
)
from services.transport_collection_service import CollectionService

router = APIRouter(
    prefix="/api/v1/collections",
    tags=["Transport Collections"],
)

@router.post("/", response_model=CollectionResponse,
             status_code=status.HTTP_201_CREATED)
def create_collection(
    data: CollectionCreate,
    db: Session = Depends(get_database),
):
    return CollectionService(db).create(data.model_dump())

@router.get("/")
def list_collections(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_database),
):
    return CollectionService(db).list(page, limit)

@router.get("/{item_id}", response_model=CollectionResponse)
def get_collection(
    item_id: int,
    db: Session = Depends(get_database),
):
    return CollectionService(db).get_by_id(item_id)

@router.patch("/{item_id}", response_model=CollectionResponse)
def update_collection(
    item_id: int,
    data: CollectionUpdate,
    db: Session = Depends(get_database),
):
    return CollectionService(db).update(
        item_id, data.model_dump(exclude_unset=True)
    )

@router.put("/{item_id}", response_model=CollectionResponse)
def replace_collection(
    item_id: int,
    data: CollectionPut,
    db: Session = Depends(get_database),
):
    return CollectionService(db).replace(
        item_id, data.model_dump()
    )

@router.delete("/{item_id}")
def delete_collection(
    item_id: int,
    db: Session = Depends(get_database),
):
    return CollectionService(db).delete(item_id)

@router.post("/{item_id}/report")
async def upload_report(
    item_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_database),
):
    return await CollectionService(db).upload_report(item_id, file)
