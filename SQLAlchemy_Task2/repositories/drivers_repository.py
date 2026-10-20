
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from models.driver_model import Driver

class DriverRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Driver:
        driver = Driver(**data)
        try:
            self.db.add(driver)
            self.db.commit()
            self.db.refresh(driver)
            return driver
        except Exception:
            self.db.rollback()
            raise

    def get_by_id(self, driver_id: int) -> Driver | None:
        return self.db.get(Driver, driver_id)

    def get_all(self, limit: int, offset: int) -> list[Driver]:
        stmt = (
            select(Driver)
            .order_by(Driver.id)
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt).all())

    def count(self) -> int:
        return self.db.scalar(
            select(func.count()).select_from(Driver)
        ) or 0

    def update(self, driver: Driver, changes: dict) -> Driver:
        try:
            for field, value in changes.items():
                setattr(driver, field, value)
            self.db.commit()
            self.db.refresh(driver)
            return driver
        except Exception:
            self.db.rollback()
            raise

    def delete(self, driver: Driver) -> None:
        try:
            self.db.delete(driver)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
