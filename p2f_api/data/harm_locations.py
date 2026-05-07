# Local libraries
from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL
from .harm_data_record import harm_data_record
from .datasets import datasets

# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Double
from sqlalchemy import Text
from sqlalchemy import Uuid
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy import ForeignKey

# Batteries included libraries
from uuid import UUID
from datetime import datetime
from zoneinfo import ZoneInfo

logger.debug(f"{fa.data} {__name__}")

class harm_locations(baseSQL):
    __tablename__ = "p2f_harm_locations"
    pk_harm_location: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    location_id: Mapped[UUID] = mapped_column(
        Uuid, default=func.gen_random_uuid(), unique=True
    )
    location_name: Mapped[str] = mapped_column(Text, nullable=True)
    location_code: Mapped[str] = mapped_column(Text, nullable=True)
    latitude: Mapped[float] = mapped_column(Double)
    longitude: Mapped[float] = mapped_column(Double)
    elevation: Mapped[float] = mapped_column(Double)
    location_age: Mapped[int] = mapped_column(BigInteger)
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )

class harm_location_to_rec(baseSQL):
    __tablename__ = "p2f_harm_location_to_rec"
    pk_harm_location_to_record: Mapped[int] = mapped_column(
        BigInteger, primary_key=True
    )
    fk_harm_location: Mapped[UUID] = mapped_column(
        ForeignKey(f"{harm_locations.__tablename__}.location_id")
    )
    fk_data_record: Mapped[str] = mapped_column(
        ForeignKey(f"{harm_data_record.__tablename__}.record_hash")
    )
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )

class harm_location_to_ds(baseSQL):
    __tablename__ = "p2f_harm_location_to_ds"
    pk_harm_location_to_record: Mapped[int] = mapped_column(
        BigInteger, primary_key=True
    )
    fk_harm_location: Mapped[UUID] = mapped_column(
        ForeignKey(f"{harm_locations.__tablename__}.location_id")
    )
    fk_dataset_id: Mapped[str] = mapped_column(
        ForeignKey(f"{datasets.__tablename__}.dataset_id")
    )
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )