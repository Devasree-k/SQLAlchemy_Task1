
from sqlalchemy import select
from sqlalchemy.orm import Session

from driver_model import Driver

    
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

    def get_all(self) -> list[Driver]:
        statement = select(Driver).order_by(Driver.driver_id)
        return list(self.db.scalars(statement).all())

    def get_by_id(self, driver_id: int) -> Driver | None:
        return self.db.get(Driver, driver_id)

    def delete(self, driver: Driver) -> None:
        try:
            self.db.delete(driver)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
