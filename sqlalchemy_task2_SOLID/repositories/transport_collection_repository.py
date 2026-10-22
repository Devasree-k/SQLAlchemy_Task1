
from sqlalchemy import select

from sqlalchemy.orm import Session, joinedload

from models.driver_model import Driver
from models.transport_collection_model import TransportCollection

from interfaces.transport_collection_repository_interface import TransportCollectionRepositoryInterface

class TransportCollectionRepository(TransportCollectionRepositoryInterface):

    def __init__(self, db: Session):
        self.db = db

    def get_driver(self, driver_id: int):
        return self.db.get(Driver, driver_id)


    def create(self, collection: TransportCollection):
        self.db.add(collection)
        self.db.flush()
        return collection


    def get_by_id(self, collection_id: int):
        statement = (
            select(TransportCollection)
            .options(joinedload(TransportCollection.driver))
            .where(TransportCollection.id == collection_id)
        )
        result = self.db.scalars(statement)

        return result.unique().first()


    def get_all(self):
        statement = (
            select(TransportCollection)
            .options(joinedload(TransportCollection.driver))
            .order_by(TransportCollection.id)
        )
        # return list(self.db.scalars(statement).unique().all())
        result = self.db.scalars(statement)

        return list(result.unique().all())

    def update_collection(
        self,
        collection: TransportCollection,
        update_data: dict,
    ) -> TransportCollection:
        for field, value in update_data.items():
            setattr(collection, field, value)

        self.db.flush()
        return collection


    def delete(self, collection: TransportCollection) -> None:
        self.db.delete(collection)
        self.db.flush()

