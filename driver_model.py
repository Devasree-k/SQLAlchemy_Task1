
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Driver(Base):
    __tablename__ = "drivers"

    driver_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    driver_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    phone_number: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        unique=True,
    )
