
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from models.driver_model import Driver

from interfaces.driver_repository_interface import DriverRepositoryInterface

class DriverRepository(DriverRepositoryInterface):

    def __init__(self, db: Session):
        self.db = db

    def create(self, driver: Driver) -> Driver:
        self.db.add(driver)     #No because it is synchrnous session-state operation.
        self.db.flush()
        return driver

    def get_by_id(self, driver_id: int):
        return self.db.get(Driver, driver_id)

    def get_all(self):
        statement = select(Driver).order_by(Driver.id)
        result = self.db.scalars(statement)
        return list(result.all())

    def get_with_collections(self, driver_id: int):
        statement = (
            select(Driver)
            .options(selectinload(Driver.collections))
            .where(Driver.id == driver_id)
        )
        result = self.db.scalars(statement)
        return result.first()

    def phone_exists(
        self,
        phone: str,
        exclude_driver_id: int | None = None,
    ) -> bool:
        statement = select(Driver.id).where(Driver.phone == phone)

        if exclude_driver_id is not None:
            statement = statement.where(
                Driver.id != exclude_driver_id
            )

        return (
            self.db.scalar(statement)
        ) is not None

