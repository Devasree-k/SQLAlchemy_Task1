
from fastapi import APIRouter, Depends, status

from dependencies.database import get_database
from schemas.transport_collection_schema import (
    CollectionCreate,
    CollectionUpdate,
    CollectionResponse,
)
from services.transport_collection_service import (
    TransportCollectionService,
)
from dependencies.service_dependencies import get_collection_service


router = APIRouter(
    prefix="/api/collections",
    tags=["Transport Collections"],
)


@router.post(
    "/",
    response_model=CollectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_collection(
    data: CollectionCreate,
    service: TransportCollectionService = Depends(
        get_collection_service
    ),
):
    return service.create_collection(data)


@router.get(
    "/",
    response_model=list[CollectionResponse],
)
def list_collections(
    service: TransportCollectionService = Depends(
        get_collection_service
    ),
):
    return service.get_collections()


@router.get(
    "/{collection_id}",
    response_model=CollectionResponse,
)
def read_collection(
    collection_id: int,
    service: TransportCollectionService = Depends(
        get_collection_service
    ),
):
    return service.get_collection(collection_id)


@router.patch(
    "/{collection_id}",
    response_model=CollectionResponse,
)
def edit_collection(
    collection_id: int,
    data: CollectionUpdate,
    service: TransportCollectionService = Depends(
        get_collection_service
    ),
):
    return service.update_collection(
        collection_id,
        data.model_dump(exclude_unset=True),
    )


@router.delete("/{collection_id}")
def remove_collection(
    collection_id: int,
    service: TransportCollectionService = Depends(
        get_collection_service
    ),
):
    return service.delete_collection(collection_id)
