
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload
from models.transport_collection_model import TransportCollection

class CollectionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> TransportCollection:
        item = TransportCollection(**data)
        try:
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            return self.get_by_id(item.id)
        except Exception:
            self.db.rollback()
            raise

    def get_by_id(self, item_id: int) -> TransportCollection | None:
        stmt = (
            select(TransportCollection)
            .options(joinedload(TransportCollection.driver))
            .where(TransportCollection.id == item_id)
        )
        return self.db.scalars(stmt).unique().first()

    def get_all(self, limit: int, offset: int) -> list[TransportCollection]:
        stmt = (
            select(TransportCollection)
            .options(joinedload(TransportCollection.driver))
            .order_by(TransportCollection.id)
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt).unique().all())

    def count(self) -> int:
        return self.db.scalar(
            select(func.count()).select_from(TransportCollection)
        ) or 0

    def update(self, item: TransportCollection, changes: dict):
        try:
            for field, value in changes.items():
                setattr(item, field, value)
            self.db.commit()
            return self.get_by_id(item.id)
        except Exception:
            self.db.rollback()
            raise

    def update_report(self, item: TransportCollection, filename: str):
        try:
            item.report_file = filename
            self.db.commit()
            return self.get_by_id(item.id)
        except Exception:
            self.db.rollback()
            raise

    def delete(self, item: TransportCollection) -> None:
        try:
            self.db.delete(item)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
