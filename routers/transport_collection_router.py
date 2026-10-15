from fastapi import (
    APIRouter,
    Depends,
    File,
    Query,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from dependencies.database import get_database
from exceptions.transport_collection_exception import (
    BadRequestException,
)
from schemas.transport_collection_schema import (
    CollectionCreate,
    CollectionUpdate,
    CollectionResponse,
)
from services.transport_collection_service import CollectionService


router = APIRouter(
    prefix="/api/v1/collections",
    tags=["Transport Collections"],
)


@router.post(
    "/",
    response_model=CollectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_collection(
    data: CollectionCreate,
    db: Session = Depends(get_database),
):
    service = CollectionService(db)
    return service.create(data.model_dump())


# @router.get("/", response_model=dict)
@router.get("/", response_model=dict[str, object])
def get_collections(
    db: Session = Depends(get_database),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=3, ge=1, le=20),
):
    service = CollectionService(db)
    return service.get_all(page, limit)


@router.get(
    "/{collection_id}",
    response_model=CollectionResponse,
)
def get_collection(
    collection_id: int,
    db: Session = Depends(get_database),
):
    service = CollectionService(db)
    return service.get_by_id(collection_id)


@router.patch(
    "/{collection_id}",
    response_model=CollectionResponse,
)
def update_collection(
    collection_id: int,
    data: CollectionUpdate,
    db: Session = Depends(get_database),
):
    changes = data.model_dump(exclude_unset=True)

    if not changes:
        raise BadRequestException(
            "Send at least one field to update"
        )

    service = CollectionService(db)

    return service.update(collection_id, changes)


@router.delete("/{collection_id}")
def delete_collection(
    collection_id: int,
    db: Session = Depends(get_database),
):
    service = CollectionService(db)
    return service.delete(collection_id)


@router.post("/{collection_id}/report")
async def upload_report(
    collection_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_database),
):
    service = CollectionService(db)

    return await service.upload_report(
        collection_id,
        file,
    )
