
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class TransportCollection(Base):
    __tablename__ = "transport_collection"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,)

    driver_name: Mapped[str] = mapped_column( String(100), nullable=False, )

    vehicle_number: Mapped[str] = mapped_column(String(20), nullable=False,)

    collection_date: Mapped[date] = mapped_column(Date, nullable=False,)

    morning_trips: Mapped[int] = mapped_column(Integer, nullable=False,)

    evening_trips: Mapped[int] = mapped_column(Integer, nullable=False,)

    morning_collection: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False,)

    evening_collection: Mapped[Decimal] = mapped_column(Numeric(10, 2),nullable=False,)

    fuel_expense: Mapped[Decimal] = mapped_column( Numeric(10, 2), nullable=False, )

    other_expense: Mapped[Decimal] = mapped_column(Numeric(10, 2),nullable=False,)

    total_trips: Mapped[int] = mapped_column(Integer, nullable=False,)

    total_collection: Mapped[Decimal] = mapped_column( Numeric(10, 2), nullable=False,)

    total_expense: Mapped[Decimal] = mapped_column( Numeric(10, 2), nullable=False,)

    net_collection: Mapped[Decimal] = mapped_column(Numeric(10, 2),nullable=False,)

    report_file: Mapped[str | None] = mapped_column(Text,nullable=True,)
