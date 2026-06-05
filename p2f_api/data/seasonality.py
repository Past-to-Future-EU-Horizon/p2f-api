# Local libraries
from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL
from .datasets import datasets
from .harm_data_record import harm_data_record

# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy import ForeignKey

# Batteries included libraries
from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import UUID

class seasonality_ds(baseSQL):
    pk_seasonality_ds: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    dataset_id: Mapped[UUID] = mapped_column(ForeignKey(f"{datasets.__tablename__}.dataset_id"))
    seasonlity_type: Mapped[str] = mapped_column(Text)
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )

class season(baseSQL):
    pk_season: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    record_hash: Mapped[str] = mapped_column(ForeignKey(f"{harm_data_record.__tablename__}.record_hash"))
    season: Mapped[str] = mapped_column(Text)
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )