    
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.transport_collection_model import TransportCollection


class CollectionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> TransportCollection:
        collection = TransportCollection(**data)

        try:
            self.db.add(collection)
            self.db.commit()
            self.db.refresh(collection)
            return collection
        except Exception:
            self.db.rollback()
            raise

    def get_by_id( self, collection_id: int,) -> TransportCollection | None:
        return self.db.get(
            TransportCollection,
            collection_id,
        )

    def get_all( self, limit: int, offset: int,) -> list[TransportCollection]:
        statement = (
            select(TransportCollection)
            .order_by(TransportCollection.id)
            .limit(limit)
            .offset(offset)
        )

        return list(self.db.scalars(statement).all())

    def get_total_count(self) -> int:
        statement = select( func.count() ).select_from(TransportCollection)
        return self.db.scalar(statement) or 0

    def update(
        self,
        collection: TransportCollection,
        changes: dict,
    ) -> TransportCollection:
        try:
            for field, value in changes.items():
                setattr(collection, field, value)

            self.db.commit()
            self.db.refresh(collection)
            return collection
        except Exception:
            self.db.rollback()
            raise

    def update_report(
        self,
        collection: TransportCollection,
        filename: str,
    ) -> TransportCollection:
        try:
            collection.report_file = filename
            self.db.commit()
            self.db.refresh(collection)
            return collection
        except Exception:
            self.db.rollback()
            raise

    def delete(self, collection: TransportCollection) -> None:
        try:
            self.db.delete(collection)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
